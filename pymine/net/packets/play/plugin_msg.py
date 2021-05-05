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

"""Contains packets relating to plugin channels and messages. See here: https://wiki.vg/Plugin_channels"""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayPluginMessageClientBound", "PlayPluginMessageServerBound")


class PlayPluginMessageClientBound(Packet):
    """Used to send a "plugin message". See here https://wiki.vg/Protocol#Plugin_Message_.28serverbound.29 (Server -> Client)

    :param str channel: The plugin channel to be used.
    :param bytes data: Data to be sent to the client.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar data:
    """

    id = 0x17
    to = 1

    def __init__(self, channel: str, data: bytes) -> None:
        super().__init__()

        self.channel = channel
        self.data = data

    def encode(self) -> bytes:
        return Buffer.pack_string(self.channel) + self.data


class PlayPluginMessageServerBound(Packet):
    """Used to send plugin data to the server (Client -> Server)

    :param str channel: The plugin channel being used.
    :param bytes data: Data to be sent to the client.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar data:
    """

    id = 0x0B
    to = 0

    def __init__(self, channel: str, data: bytes) -> None:
        super().__init__()

        self.channel = channel
        self.data = data

    def decode(self, buf: Buffer) -> PlayPluginMessageServerBound:
        return PlayPluginMessageServerBound(buf.unpack_string(), Buffer(buf.read()))
