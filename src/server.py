
from src.logic.status import status as server_func_status
from src.data.states import *
from src.types.packet import Packet
from src.types.buffer import Buffer
from src.data.server_properties import *
from src.data.packet_map import PACKET_MAP
from src.types.packets.handshaking.legacy_ping import HandshakeLegacyPingRequest
import immutables
import logging
import asyncio
import base64
import sys
import os
sys.path.append(os.getcwd())
# import uvloop


global share
share = {
    'version': '1.16.4',
    'protocol': 754,
    'timeout': .15
}

try:  # Load server.properties
    with open('server.properties', 'r+') as f:
        lines = f.readlines()

        share['PROPERTIES'] = dict(SERVER_PROPERTIES)
        share['PROPERTIES'].update(parse_properties(lines))
        share['PROPERTIES'] = immutables.Map(PROPERTIES)
except Exception:
    with open('server.properties', 'w+') as f:
        f.write(SERVER_PROPERTIES_BLANK)

    share['PROPERTIES'] = SERVER_PROPERTIES

try:  # Load favicon
    with open('server-icon.png', 'rb') as favicon:
        share['favicon'] = 'data:image/png;base64,' + \
            base64.b64encode(favicon.read()).decode('utf-8')
except Exception:
    share['favicon'] = None

states = {}  # {remote_address: state_id}
share['states'] = states

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def handle_packet(r: asyncio.StreamReader, w: asyncio.StreamWriter, remote: tuple):
    read = await r.read(1)

    if read == b'\xFE':
        return HandshakeLegacyPingRequest.decode(Buffer(await asyncio.wait_for(r.read(200), share['timeout'])))

    buf = Buffer(read)

    try:
        for i in range(4):
            buf.write(await asyncio.wait_for(p.read(1), share['timeout']))
    except Exception:
        pass

    buf.write(await r.read(buf.unpack_varint()))

    state = STATES_BY_ID[states.get(remote, 0)]
    packet = buf.unpack_packet(state, 0, PACKET_MAP)

    logger.debug(f'state:{state} | id_:{packet.id_} | packet:{type(packet)}')

    if state == 'handshaking':
        states[remote] = packet.next_state
        await handle_packet(r, w, remote)
    elif state == 'status':
        if packet.id_ == 0x00:  # StatusStatusRequest
            await server_func_status(r, w, packet, share)


async def handle_con(r, w):
    remote = w.get_extra_info('peername')  # (host, port)
    logger.info(f'Connection received from {remote[0]}:{remote[1]}')

    await handle_packet(r, w, remote)


async def start():
    port = 69
    server = await asyncio.start_server(handle_con, port=port)

    try:
        async with server:
            print(f'Server started on port {port}')
            await server.serve_forever()
    except KeyboardInterrupt:
        pass

# uvloop.install()
asyncio.run(start())
