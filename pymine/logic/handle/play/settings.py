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

from pymine.types.stream import Stream
from pymine.types.packet import Packet
from pymine.logic.join import join_2
from pymine.server import server


@server.api.register.on_packet("play", 0x05)
async def client_settings_recv(stream: Stream, packet: Packet) -> None:
    player = await server.playerio.fetch_player(server.cache.uuid[stream.remote])

    player.locale = packet.locale
    player.view_distance = packet.view_distance
    player.chat_mode = packet.chat_mode
    player.chat_colors = packet.chat_colors
    player.displayed_skin_parts = packet.displayed_skin_parts
    player.main_hand = packet.main_hand

    # await join_2(stream, player)
