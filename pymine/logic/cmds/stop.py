from pymine.util.stop import stop
from pymine.server import server


@server.api.commands.on_command(name="stop", node="minecraft.cmd.stop")
async def stop_server(uuid):
    await stop(server)
