from pymine.server import server


@server.api.commands.on_command(name="stop", node="minecraft.cmd.list")
async def list(uuid):
    self.console.info(
        f"There are {len(server.playerio.cache)}/{server.conf['max_players']} online: {', '.join([p.username for p in server.playerio.cache.values()])}"
    )
