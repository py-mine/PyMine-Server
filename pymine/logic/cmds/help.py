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

import inspect
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

    equal_signs = "=" * min(25, os.get_terminal_size().columns // 4)
    server.console.info(f"{equal_signs} HELP {equal_signs}")

    for name, command in server.api.commands._commands.items():
        func, node = command
        doc = getattr(func, "__doc__")
        server.console.info(f"{name}: {'Documentation missing.' if doc is None else doc}")

        if func.__code__.co_argcount > 1:
            server.console.info(" Arguments:")
            argspec = inspect.getfullargspec(func)

            # XXX: Causes errors / incorrect behaviour if you introduce other mandatory arguments
            for arg in argspec.args[1:]:  # Skipping the first 'uuid'
                # look at this mess
                ann = (
                    (
                        ": "
                        + (
                            argspec.annotations[arg].__name__
                            if hasattr(argspec.annotations[arg], "__name__")
                            else argspec.annotations[arg].__class__.__name__
                        )
                    )
                    if arg in argspec.annotations.keys()
                    else ""
                )

                server.console.info(" - " + arg + ann)
