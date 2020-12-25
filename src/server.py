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


async def handle_con(r, w):
    # buf = Buffer(await r.read(5))  # Varint is no longer than 5 bytes, so 1st 5 are always required
    # buf.add(await r.read(buf.unpack_varint()))  # Read the rest of the packet
    # buf.reset()  # Reset position in buf back to 0

    buf = Buffer(await r.read())

    remote_address = w.get_extra_info('peername')
    packet = buf.unpack_packet(STATES_BY_ID[states.get(remote_address, 0)])

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
