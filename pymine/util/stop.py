import asyncio

async def stop(server):
    server.server.close()
    await server.server.wait_closed()

    if server.uvloop:  # uvloop is a difficult little shit *sigh*
        asyncio.get_event_loop().stop()
