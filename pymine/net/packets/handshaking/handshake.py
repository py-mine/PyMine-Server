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
            
"""Contains HandshakeHandshake, a packet for starting the connection between the server and client."""

from __future__ import annotations

from pymine.types.buffer import Buffer
from pymine.types.packet import Packet

__all__ = ("HandshakeHandshake",)


class HandshakeHandshake(Packet):
    """Initiates the connection between the server and client. (Client -> Server)

    :param int protocol: Protocol version to be used.
    :param str address: The host/address the client is connecting to.
    :param int port: The port the client is connection on.
    :param int next_state: The next state which the server should transfer to. 1 for status, 2 for login.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar protocol:
    :ivar address:
    :ivar port:
    :ivar next_state:
    """

    id = 0x00
    to = 0

    def __init__(self, protocol: int, address: str, port: int, next_state: int) -> None:
        super().__init__()

        self.protocol = protocol
        self.address = address
        self.port = port
        self.next_state = next_state

    @classmethod
    def decode(cls, buf: Buffer) -> HandshakeHandshake:
        return cls(buf.unpack_varint(), buf.unpack_string(), buf.unpack("H"), buf.unpack_varint())
