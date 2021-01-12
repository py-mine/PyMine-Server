from cryptography.hazmat.primitives.asymmetric import rsa
import asyncio
import aiohttp
import random
import struct

import sys
import os

sys.path.append(os.getcwd())  # nopep8

import src.api as pymine_api

from src.types.buffer import Buffer

from src.data.packet_map import PACKET_MAP
from src.data.states import STATES

from src.util.logging import task_exception_handler
from src.util.share import share, logger

share['rsa']['private'] = rsa.generate_private_key(65537, 1024)
share['rsa']['public'] = share['rsa']['private'].public_key()

states = share['states']
logger.debug_ = share['conf']['debug']


async def close_con(w, remote):  # Close a connection to a client
    await w.drain()

    w.close()
    await w.wait_closed()

    try:
        del states[remote]
    except BaseException:
        pass

    logger.debug(f'Disconnected nicely from {remote[0]}:{remote[1]}.')
    return False, None, w

share['close_con'] = close_con


# Handle / respond to packets, this is a loop
async def handle_packet(r: asyncio.StreamReader, w: asyncio.StreamWriter, remote: tuple):
    packet_length = 0

    # Basically an implementation of Buffer.unpack_varint()
    # except designed to read directly from a a StreamReader
    # and also to handle legacy server list ping packets
    for i in range(5):
        try:
            read = await asyncio.wait_for(r.read(1), 5)
        except asyncio.TimeoutError:
            return await close_con(w, remote)

        if i == 0 and read == b'\xFE':
            logger.warn('Legacy ping attempted, legacy ping is not supported.')
            return False, r, w

        b = struct.unpack('B', read)[0]
        packet_length |= (b & 0x7F) << 7 * i

        if not b & 0x80:
            break

    if packet_length & (1 << 31):
        packet_length -= 1 << 32

    buf = Buffer(await r.read(packet_length))

    state = STATES.encode(states.get(remote, 0))
    packet = buf.unpack_packet(state, 0, PACKET_MAP)

    logger.debug(f'IN : state:{state:<11} | id:0x{packet.id:02X} | packet:{type(packet).__name__}')

    for handler in pymine_api.PACKET_HANDLERS[state][packet.id]:
        resp_value = await handler(r, w, packet, remote)

        try:
            continue_, r, w = resp_value
        except (ValueError, TypeError,):
            logger.warn(f'Invalid return from handler: {handler}')
            continue

        if not continue_:
            return False, r, w

    return continue_, r, w


async def handle_con(r, w):  # Handle a connection from a client
    remote = w.get_extra_info('peername')  # (host, port,)
    logger.debug(f'connection received from {remote[0]}:{remote[1]}.')

    continue_ = True

    while continue_:
        try:
            continue_, r, w = await handle_packet(r, w, remote)
        except BaseException as e:
            logger.error(logger.f_traceback(e))
            break

    await close_con(w, remote)


async def start():  # Actually start the server
    addr = share['conf']['server_ip']
    port = share['conf']['server_port']

    server = share['server'] = await asyncio.start_server(handle_con, host=addr, port=port)

    await pymine_api.init()

    try:
        async with aiohttp.ClientSession() as share['ses']:
            async with server:
                if random.randint(0, 999) == 1:  # shhhhh
                    logger.info(f'PPMine 69.0 started on port {addr}:{port}!')
                else:
                    logger.info(
                        f'PyMine {float(share["server_version"])} started on {addr}:{port}!')

                await server.serve_forever()
    except (asyncio.CancelledError, KeyboardInterrupt,):
        logger.info('Closing server...')

        await pymine_api.stop()

        logger.info('Server closed.')


loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.set_exception_handler(task_exception_handler)

try:
    loop.run_until_complete(start())
except BaseException as e:
    logger.critical(logger.f_traceback(e))
