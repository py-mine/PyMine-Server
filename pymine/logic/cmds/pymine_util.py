from pymine.logic.parsers.brigadier import *

from pymine.util.misc import nice_eval

from pymine.server import server


@server.api.commands.on_command(name="eval", node="pymine.cmds.eval")
async def eval_(uuid, text: String(2)):
    try:
        server.console.info(await nice_eval(text, {"server": server}))
    except BaseException as e:
        server.console.error(server.console.f_traceback(e))


@server.api.commands.on_command(name="test", node="pymine.cmds.test")
async def test(uuid, b: Bool, f: Float(), d: Double(), i: Integer(), s: str, s2: String(1), s3: String(2)):
    print(uuid, b, f, d, i, s, s2, s3)


# @server.api.commands.on_command(name="exec", node="pymine.cmds.exec")
# async def exec_(uuid: str, file_name: str):
#
#     try:
#         with open(file_name, "r") as f:
#             cmds_lines = [l.rstrip("\n") for l in f.readlines()]
#
#             for cmd_line in cmds_lines:
#                 await server.api.commands.server_command(cmd_line)
#
#     except FileNotFoundError:
#         server.console.warn("Can't find that file...")
#
#
# @server.api.commands.on_command(name="eval", node="pymine.cmds.eval")
# async def eval_(uuid: str, text: str):
#     try:
#         server.console.info(repr(eval(text)))
#     except BaseException as e:
#         server.console.error(server.console.f_traceback(e))
#
#
# @server.api.commands.on_command(name="awaiteval", node="pymine.cmds.eval")
# async def awaiteval(uuid: str, text: str):
#     try:
#         server.console.info(repr(await eval(text)))
#     except BaseException as e:
#         server.console.error(server.console.f_traceback(e))
#
#
# @server.api.commands.on_command(name="echo", node="pymine.cmds.echo")
# async def echo(uuid: str, text: str):
#     server.console.info(f"{uuid}: {text}")
#
#
@server.api.commands.on_command(name="help", node="pymine.cmds.help")
async def help(uuid: str):
    server.console.info(
        """===============HELP===============
help - Lists common commands and usage.
eval - Evaluate the arguments as python code.(Not necessary if debug_mode is True)"""
    )
