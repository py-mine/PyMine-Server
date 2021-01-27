import asyncio

from pymine.server import server


@server.api.commands.on_command(name="stop", node="minecraft.cmd.stop")
async def stop_server(uuid: str, args: str):
    server.server.close()
    await server.server.wait_closed()

    if server.uvloop:  # uvloop is difficult *sigh*
        asyncio.get_event_loop().stop()
