
import immutables
import logging
import asyncio
import base64
import sys
import os
# import uvloop

sys.path.append(os.getcwd())

from src.types.packets.handshaking.legacy_ping import HandshakeLegacyPingRequest  # nopep8
from src.data.packet_map import PACKET_MAP  # nopep8
from src.data.server_properties import *  # nopep8
from src.types.buffer import Buffer  # nopep8
from src.types.packet import Packet  # nopep8
from src.data.states import *  # nopep8

from src.logic.status import status as server_func_status  # nopep8
from src.logic.status import pong as server_func_pong  # nopep8

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
    share['favicon'] = 'data:image/png;base64,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'

states = {}  # {remote_address: state_id}
share['states'] = states

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def handle_packet(r: asyncio.StreamReader, w: asyncio.StreamWriter, remote: tuple):
    read = await r.read(1)

    if read == b'\xFE':
        return HandshakeLegacyPingRequest.decode(Buffer(read + await asyncio.wait_for(r.read(200), share['timeout'])))

    buf = Buffer(read)

    try:
        for i in range(4):
            buf.write(await asyncio.wait_for(p.read(1), share['timeout']))
    except Exception:
        pass

    buf.write(await r.read(buf.unpack_varint()))

    state = STATES_BY_ID[states.get(remote, 0)]
    packet = buf.unpack_packet(state, 0, PACKET_MAP)

    logger.debug(f'state:{state:<12} | id_:{packet.id_:<3} | packet:{packet.__class__.__name__}')

    if state == 'handshaking':
        states[remote] = packet.next_state
        await handle_packet(r, w, remote)
    elif state == 'status':
        if packet.id_ == 0x00:  # StatusStatusRequest
            await server_func_status(r, w, packet, share)
        elif packet.id_ == 0x01:  # StatusStatusPingPong
            await server_func_pong(r, w, packet)


async def handle_con(r, w):
    remote = w.get_extra_info('peername')  # (host, port)
    logger.info(f'Connection received from {remote[0]}:{remote[1]}')

    await handle_packet(r, w, remote)

    w.close()
    await w.wait_closed()
    del states[remote]


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
