from cryptography.hazmat.primitives.asymmetric import rsa
import immutables
import logging
import asyncio
import random
import sys
import os
# import uvloop

sys.path.append(os.getcwd())

from src.types.packets.handshaking.legacy_ping import HandshakeLegacyPingRequest  # nopep8
from src.data.packet_map import PACKET_MAP  # nopep8
from src.types.buffer import Buffer  # nopep8
from src.types.packet import Packet  # nopep8
from src.data.states import *  # nopep8
from src.data.config import *  # nopep8

from src.logic.status import status as logic_status  # nopep8
from src.logic.status import pong as logic_pong  # nopep8

global share
share = {
    'server_version': 1,
    'version': '1.16.4',
    'protocol': 754,
    'timeout': .15,
    'rsa': {  # https://stackoverflow.com/questions/54495255/python-cryptography-export-key-to-der
        'private': rsa.generate_private_key(65537, 1024),
        'public': None
    },
    'properties': SERVER_PROPERTIES,
    'favicon': FAVICON
}

share['rsa']['public'] = share['rsa']['private'].public_key()

states = {}  # {remote_address: state_id}
share['states'] = states

logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.DEBUG,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
logger = logging.getLogger(__name__)
share['logger'] = logger


async def handle_packet(r: asyncio.StreamReader, w: asyncio.StreamWriter, remote: tuple):
    buf = Buffer(await r.read(1))

    if buf.buf == b'\xFE':
        raise NotImplementedError('legacy ping is not currently supported.')

    try:
        for i in range(4):
            buf.write(await asyncio.wait_for(p.read(1), share['timeout']))
    except Exception:
        pass

    buf.write(await r.read(buf.unpack_varint()))

    state = STATES_BY_ID[states.get(remote, 0)]
    packet = buf.unpack_packet(state, 0, PACKET_MAP)

    logger.debug(f'state:{state:<12} | id:{hex(packet.id_):<4} | packet:{type(packet).__name__}')

    if state == 'handshaking':
        states[remote] = packet.next_state
        await handle_packet(r, w, remote)
    elif state == 'status':
        if packet.id_ == 0x00:  # StatusStatusRequest
            await logic_status(r, w, packet, share)
        elif packet.id_ == 0x01:  # StatusStatusPingPong
            await logic_pong(r, w, packet)
    elif state == 'login':
        pass


async def handle_con(r, w):
    remote = w.get_extra_info('peername')  # (host, port)
    logger.debug(f'connection received from {remote[0]}:{remote[1]}')

    await handle_packet(r, w, remote)

    w.close()
    await w.wait_closed()
    del states[remote]


async def start():
    port = 69
    server = await asyncio.start_server(handle_con, port=port)

    try:
        async with server:
            if random.randint(0, 999) == 1:
                logger.info(f'PPMine 69 started on port {port}!')
            else:
                logger.info(f'PyMine {share["server_version"]} started on port {port}!')

            await server.serve_forever()
    except KeyboardInterrupt:
        pass

# uvloop.install()
asyncio.run(start())
