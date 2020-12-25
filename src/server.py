import asyncio
import uvloop


async def handle_con(reader, writer):
    pass


async def start():
    server = await asyncio.start_server(handle_con, port=69)

    async with server:
        await server.serve_forever()

uvloop.install()
asyncio.run(start())
