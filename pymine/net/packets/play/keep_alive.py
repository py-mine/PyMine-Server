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

"""Contains packets for maintaining the connection between client and server."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayKeepAliveClientBound",
    "PlayKeepAliveServerBound",
)


class PlayKeepAliveClientBound(Packet):
    """Sent by the server in order to maintain connection with the client. (Server -> Client)

    :param int keep_alive_id: A randomly generated (by the server) integer/long.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar keep_alive_id:
    """

    id = 0x1F
    to = 1

    def __init__(self, keep_alive_id: int) -> None:
        super().__init__()

        self.keep_alive_id = keep_alive_id

    def encode(self) -> bytes:
        return Buffer.pack("q", self.keep_alive_id)


class PlayKeepAliveServerBound(Packet):
    """Sent by client in order to maintain connection with server. (Client -> Server)

    :param int keep_alive_id: A randomly generated (by the server) integer/long.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar keep_alive_id:
    """

    id = 0x10
    to = 0

    def __init__(self, keep_alive_id: int) -> None:
        super().__init__()

        self.keep_alive_id = keep_alive_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayKeepAliveServerBound:
        return cls(buf.unpack("q"))
