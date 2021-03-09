import os

from pymine.server import server

# @server.api.commands.on_command(name="help", node="pymine.cmds.help")
# async def help(uuid: str):
#     server.console.info(
#         """===============HELP===============
# help - Lists common commands and usage.
# eval - Evaluate the arguments as python code.(Not necessary if debug_mode is True)"""
#     )


@server.api.commands.on_command(name="help", node="pymine.cmds.help")
async def help(uuid: str):
    """Shows this message."""

    equal_signs = '='*min(25, os.get_terminal_size().columns//4)
    server.console.info(f"{equal_signs} HELP {equal_signs}")

    for name, command in server.api.commands._commands.items():
        func, node = command
        doc = getattr(func, "__doc__")
        server.console.info(f"{name}: {'A command.' if doc is None else doc}")
