from cryptography.hazmat.primitives.asymmetric import rsa
import immutables
import asyncio
import aiohttp
import random
import struct
import sys
import os

sys.path.append(os.getcwd())

from src.types.buffer import Buffer  # nopep8
from src.types.packet import Packet  # nopep8

from src.data.packet_map import PACKET_MAP  # nopep8
from src.data.states import *  # nopep8

from src.logic.login import set_compression as logic_login_set_compression  # nopep8
from src.logic.login import request_encryption as logic_request_encryption  # nopep8
from src.logic.commands import handle_server_commands, load_commands  # nopep8
from src.logic.login import login_success as logic_login_success  # nopep8
from src.logic.login import server_auth as logic_server_auth  # nopep8
from src.logic.login import login_kick as logic_login_kick  # nopep8
from src.logic.status import status as logic_status  # nopep8
from src.logic.status import pong as logic_pong  # nopep8
from src.logic.lan_support import ping_lan  # nopep8

import src.util.encryption as encryption  # nopep8
from src.util.share import *  # nopep8

load_commands()

share['rsa']['private'] = rsa.generate_private_key(65537, 1024)
share['rsa']['public'] = share['rsa']['private'].public_key()

states = share['states']
login_cache = {}  # {remote: {username: username, verify_token: verify_token]}
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
            logger.warn('Legacy ping is not supported currently.')
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

    logger.debug(
        f'IN : state:{state:<11} | id:{hex(packet.id_):<4} | packet:{type(packet).__name__}'
    )

    if state == 'handshaking':
        states[remote] = packet.next_state
    elif state == 'status':
        if packet.id_ == 0x00:  # StatusStatusRequest
            await logic_status(r, w, packet)
        elif packet.id_ == 0x01:  # StatusStatusPingPong
            await logic_pong(r, w, packet)
            return await close_con(w, remote)
    elif state == 'login':
        if packet.id_ == 0x00:  # LoginStart
            if share['conf']['online_mode']:
                login_cache[remote] = {'username': packet.username, 'verify': None}
                await logic_request_encryption(r, w, packet, login_cache[remote])
            else:  # If no auth is used, go straight to login success
                await logic_login_success(r, w, packet.username)
        elif packet.id_ == 0x01:  # LoginEncryptionResponse
            shared_key, auth = await logic_server_auth(packet, remote, login_cache[remote])

            del login_cache[remote]

            if not auth:
                await logic_login_kick(w)
                return await close_con(w, remote)

            # Generate a cipher for that client using the shared key from the client
            cipher = encryption.gen_aes_cipher(shared_key)

            # Replace streams with ones which auto decrypt + encrypt data when reading/writing
            r = encryption.EncryptedStreamReader(r, cipher.decryptor())
            w = encryption.EncryptedStreamWriter(w, cipher.encryptor())

            if share['comp_thresh'] > 0:  # Send set compression packet if needed
                await logic_login_set_compression(w)

            await logic_login_success(r, w, *auth)

            states[remote] = 3  # PLAY
    elif state == 'play':
        logger.debug('entered play state!')

    # Return whether handle_con should continue handling packets,
    # as well as the same StreamReader and StreamWriter just in
    # case they have been replaced by encrypted versions
    return True, r, w


async def handle_con(r, w):  # Handle a connection from a client
    remote = w.get_extra_info('peername')  # (host, port,)
    logger.debug(f'connection received from {remote[0]}:{remote[1]}')

    c = True

    while c:
        c, r, w = await handle_packet(r, w, remote)


async def start():  # Actually start the server
    addr = share['conf']['server_ip']
    port = share['conf']['server_port']

    server = share['server'] = await asyncio.start_server(handle_con, host=addr, port=port)

    cmd_task = asyncio.create_task(handle_server_commands())  # Used to handle commands
    lan_support_task = asyncio.create_task(ping_lan())  # Adds lan support

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
        lan_support_task.cancel()

        logger.info('Server closed.')

try:
    asyncio.run(start())
except BaseException as e:
    logger.critical(logger.f_traceback(e))
