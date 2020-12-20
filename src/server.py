import asyncio

async def handle_con(*args):
    print(args)

async def start():
    server = await asyncio.start_server(port=25565)

    async with server:
        await server.serve_forever()

asyncio.get_event_loop().run_until_complete(start())
