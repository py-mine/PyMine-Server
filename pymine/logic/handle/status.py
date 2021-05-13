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

import pymine.net.packets.status.status as status_packets
from pymine.api.errors import StopHandling
from pymine.types.stream import Stream
from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chat import Chat
from pymine.server import server


@server.api.register.on_packet("status", 0x00)
async def send_status(stream: Stream, packet: Packet) -> tuple:
    data = {
        "version": {"name": server.meta.version, "protocol": server.meta.protocol},
        "players": {
            "max": server.conf["max_players"],
            "online": len(server.playerio.cache),
            "sample": [{"name": p.username, "id": str(p.uuid)} for p in server.playerio.cache.values()],
        },
        "description": Chat(server.conf["motd"]).msg,  # a Chat
    }

    if server.favicon:
        data["favicon"] = server.favicon

    await server.send_packet(stream, status_packets.StatusStatusResponse(data), -1)


@server.api.register.on_packet("status", 0x01)
async def send_pong(stream: Stream, packet: Packet) -> tuple:
    await server.send_packet(stream, packet, -1)
    raise StopHandling
