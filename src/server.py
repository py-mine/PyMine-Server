import asyncio
import uvloop

from src.data.packet_map import PACKET_MAP
from src.types.buffer import Buffer


async def status(r, w):


async def handle_con(r, w):
    buf = Buffer(await r.read(5))  # Varint is no longer than 5 bytes, so 1st 5 are always required
    buf.add(await r.read(buf.unpack_varint()))  # Read the rest of the packet
    buf.reset()  # Reset position in buf back to 0

    packet = buf.unpack_packet()


async def start():
    server = await asyncio.start_server(handle_con, port=69)

    async with server:
        await server.serve_forever()

uvloop.install()
asyncio.run(start())
