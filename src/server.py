from cryptography.hazmat.primitives.asymmetric import rsa
import immutables
import asyncio
import aiohttp
import random
import struct
import sys
import os
# import uvloop

sys.path.append(os.getcwd())

from src.data.packet_map import PACKET_MAP  # nopep8
from src.types.buffer import Buffer  # nopep8
from src.types.packet import Packet  # nopep8
from src.data.states import *  # nopep8
from src.data.config import *  # nopep8

from src.logic.login import request_encryption as logic_request_encryption  # nopep8
from src.logic.login import login_success as logic_login_success  # nopep8
from src.logic.login import server_auth as logic_server_auth  # nopep8
from src.logic.status import status as logic_status  # nopep8
from src.logic.status import pong as logic_pong  # nopep8
from src.logic.commands import handle_commands  # nopep8

from src.util.share import share, logger  # nopep8

share.update({
    'server_version': 1,
    'version': '1.16.4',
    'protocol': 754,
    'timeout': .15,
    'rsa': {  # https://stackoverflow.com/questions/54495255/python-cryptography-export-key-to-der
        'private': rsa.generate_private_key(65537, 1024),
        'public': None
    },
    'properties': SERVER_PROPERTIES,
    'favicon': FAVICON,
    'ses': None
})

share['rsa']['public'] = share['rsa']['private'].public_key()

states = {}  # {remote: state_id}
share['states'] = states

secrets = {}  # {remote: secret}
share['secrets'] = secrets

login_cache = {}  # {remote: [username, verify_token]}

logger.debug_ = SERVER_PROPERTIES['debug']


async def close_con(w, remote):
    w.close()
    await w.wait_closed()

    try:
        del states[remote]
    except BaseException:
        pass


async def handle_packet(r: asyncio.StreamReader, w: asyncio.StreamWriter, remote: tuple):
    packet_length = 0

    for i in range(5):
        try:
            read = await asyncio.wait_for(r.read(1), 1)
        except asyncio.TimeoutError:
            return await close_con(w, remote)

        if i == 0 and read == b'\xFE':
            logger.warning('legacy ping is not supported currently.')
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
        f'IN : state:{state:<11} | id:{hex(packet.id_):<4} | packet:{type(packet).__name__}')

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
            if SERVER_PROPERTIES['online_mode']:
                login_cache[remote] = {'username': packet.username, 'verify': None}
                await logic_request_encryption(r, w, packet, login_cache[remote])
            else:
                await logic_login_success(r, w, packet.username)
        elif packet.id_ == 0x01:  # LoginEncryptionResponse
            uuid, name = await logic_server_auth(packet, remote, username_cache[remote])
            del username_cache[remote]

            if share['rsa']['private'].decrypt()

    asyncio.create_task(handle_packet(r, w, remote))


async def handle_con(r, w):
    remote = w.get_extra_info('peername')  # (host, port)
    logger.debug(f'connection received from {remote[0]}:{remote[1]}')

    await handle_packet(r, w, remote)


async def start():
    addr = SERVER_PROPERTIES['server_ip']
    port = SERVER_PROPERTIES['server_port']

    server = await asyncio.start_server(handle_con, host=addr, port=port)

    asyncio.create_task(handle_commands())

    try:
        async with aiohttp.ClientSession() as share['ses']:
            async with server:
                if random.randint(0, 999) == 1:
                    logger.info(f'PPMine 69.0 started on port {addr}:{port}!')
                else:
                    logger.info(
                        f'PyMine {float(share["server_version"])} started on {addr}:{port}!')

                await server.serve_forever()
    except KeyboardInterrupt:
        server.close()
        await server.wait_closed()

# uvloop.install()
asyncio.run(start())
