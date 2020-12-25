import logging
import asyncio
import sys
import os
# import uvloop

sys.path.append(os.getcwd())

from src.data.packet_map import PACKET_MAP
from src.types.packet import Packet
from src.types.buffer import Buffer
from src.data.states import *

states = {}  # {remote_address: state_id}

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def handle_con(r, w):
    remote = w.get_extra_info('peername')  # (host, port)
    logger.info(f'Connection received from {remote[0]}:{remote[1]}')

    read = await r.read(1)  # Read first byte

    if read.startswith(b'\xFE'):  # Legacy ping
        raise NotImplemented

    # Varint can be no longer than 5 bytes, so first 5 bytes are pretty much guaranteed
    read += await r.read(4)
    buf.write(await r.read(Buffer(read).unpack_varint()))  # Read the rest of the packet

    packet = buf.unpack_packet(STATES_BY_ID[states.get(remote, 0)], PACKET_MAP)

    print(type(packet))
    print(packet.__dict__)


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
