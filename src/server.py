import asyncio

async def handle_con(reader, writer):
    pass

async def start():
    server = await asyncio.start_server(handle_con, port=69)

    async with server:
        await server.serve_forever()

asyncio.get_event_loop().run_until_complete(start())
