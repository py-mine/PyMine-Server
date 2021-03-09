from pymine import server

@server.api.commands.on_command(name="help", node="pymine.cmds.help")
async def help(uuid: str):
    server.console.info(
        """===============HELP===============
help - Lists common commands and usage.
eval - Evaluate the arguments as python code.(Not necessary if debug_mode is True)"""
    )
