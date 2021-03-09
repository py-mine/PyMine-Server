from pymine.logic.parsers.brigadier import *

from pymine.util.misc import nice_eval

from pymine.server import server


@server.api.commands.on_command(name="eval", node="pymine.cmds.eval")
async def eval_(uuid, text: String(2)):
    """Evaluates input as code."""

    try:
        server.console.info(await nice_eval(text, {"server": server}))
    except BaseException as e:
        server.console.error(server.console.f_traceback(e))


@server.api.commands.on_command(name="test", node="pymine.cmds.test")
async def test(uuid, b: Bool, f: Float(), d: Double(), i: Integer(), s: str, s2: String(1), s3: String(2)):
    print(uuid, b, f, d, i, s, s2, s3)
