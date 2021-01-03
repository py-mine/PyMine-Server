from cryptography.hazmat.primitives.asymmetric import rsa
import asyncio
import aiohttp
import random
import struct
import sys
import os

sys.path.append(os.getcwd())

from src.types.buffer import Buffer  # nopep8

from src.data.packet_map import PACKET_MAP  # nopep8
from src.data.states import *  # nopep8

from src.logic.commands import handle_server_commands, load_commands  # nopep8
from src.logic.status import legacy_ping as logic_legacy_ping  # nopep8
from src.logic.status import status as logic_status  # nopep8
from src.logic.login import login as logic_login  # nopep8
from src.logic.play import play as logic_play  # nopep8

from src.util.share import share, logger  # nopep8

load_commands()

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
            await logic_legacy_ping(r, w, remote)
            return await close_con(w, remote)

        b = struct.unpack('B', read)[0]
        packet_length |= (b & 0x7F) << 7 * i

        if not b & 0x80:
            break

    if packet_length & (1 << 31):
        packet_length -= 1 << 32

    buf = Buffer(await r.read(packet_length))

    state = STATES_BY_ID[states.get(remote, 0)]
    packet = buf.unpack_packet(state, 0, PACKET_MAP)

    logger.debug(f'IN : state:{state:<11} | id:0x{packet.id:02X} | packet:{type(packet).__name__}')

    if state == 'handshaking':
        states[remote] = packet.next_state
        return True, r, w

    if state == 'status':
        return await logic_status(r, w, packet, remote)

    if state == 'login':
        return await logic_login(r, w, packet, remote)

    if state == 'play':
        return await logic_play(r, w, packet, remote)


async def handle_con(r, w):  # Handle a connection from a client
    remote = w.get_extra_info('peername')  # (host, port,)
    logger.debug(f'connection received from {remote[0]}:{remote[1]}.')

    c = True

    while c:
        try:
            c, r, w = await handle_packet(r, w, remote)
        except BaseException as e:
            logger.error(logger.f_traceback(e))
            break

    await close_con(w, remote)


async def start():  # Actually start the server
    addr = share['conf']['server_ip']
    port = share['conf']['server_port']

    server = share['server'] = await asyncio.start_server(handle_con, host=addr, port=port)

    cmd_task = asyncio.create_task(handle_server_commands())  # Used to handle commands

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

        cmd_task.cancel()

        logger.info('Server closed.')

try:
    asyncio.run(start())
except BaseException as e:
    logger.critical(logger.f_traceback(e))
