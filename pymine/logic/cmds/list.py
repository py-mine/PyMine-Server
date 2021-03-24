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
            
from pymine.server import server


@server.api.commands.on_command(name="list", node="minecraft.cmd.list")
async def list(uuid):
    """Lists the players online on the server."""

    players_online = len(server.playerio.cache)

    if players_online > 0:
        server.console.info(
            f"There are {players_online}/{server.conf['max_players']} players online: {', '.join([p.username for p in server.playerio.cache.values()])}"
        )
    else:
        server.console.info(f"There are {players_online}/{server.conf['max_players']} players online.")
