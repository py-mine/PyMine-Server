# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
