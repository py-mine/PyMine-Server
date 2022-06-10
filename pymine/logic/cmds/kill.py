# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2022 PyMine

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

from pymine.server import server


@server.api.commands.on_command(name="kill", node="minecraft.cmd.kill")
async def kill(uuid, name: str):
    """Kills a player."""

    server.console.info(f"Kill was executed. {uuid=}, {name=}")
    server.console.info(f"{server.playerio.cache=}")

    player = None
    
    for i in server.playerio.cache.values():
        if i.username == name:
            player = i
            break
    else:
        server.console.error("No player with username \"" + name + "\" found.")
        return

    server.console.info(player.stream)
