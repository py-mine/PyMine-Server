from pymine.server import server


@server.api.events.on_command(name="stop", node="minecraft.cmd.stop")
async def stop_server(uuid: str, args: str):
    server.close()
