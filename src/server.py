import asyncio
import uvloop

from src.data.packet_map import PACKET_MAP


async def handle_con(r, w):
    pass


async def start():
    server = await asyncio.start_server(handle_con, port=69)

    async with server:
        await server.serve_forever()

uvloop.install()
asyncio.run(start())
