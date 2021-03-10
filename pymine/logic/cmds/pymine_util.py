from pymine.logic.parsers.brigadier import *

from pymine.util.chunk import dump_to_obj
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


@server.api.commands.on_command(name="testworldgen", node="pymine.cmds.testworldgen")
async def test_world_gen(uuid):
    chunk = await server.worlds["minecraft:overworld"].fetch_chunk(0, 0)

    with open("chunk_test.obj", "w+") as f:
        dump_to_obj(f, chunk)
