from pymine.server import server


@server.api.commands.on_command(name="list", node="minecraft.cmd.list")
async def list(uuid):
    players_online = len(server.playerio.cache)

    if players_only > 0:
        server.console.info(
            f"There are {players_online}/{server.conf['max_players']} players online: {', '.join([p.username for p in server.playerio.cache.values()])}"
        )
    else:
        server.console.info(f"There are {players_online}/{server.conf['max_players']} players online.")
