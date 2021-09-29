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

"""Contains packets related to signs."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayUpdateSign",)


class PlayUpdateSign(Packet):
    """Sent from the client when the done button is pressed in the sign GUI. (Client -> Server)

    :param int x: The x coordinate of the sign.
    :param int y: The y coordinate of the sign.
    :param int z: The z coordinate of the sign.
    :param str line_1: Line 1 on the sign.
    :param str line_2: Line 2 on the sign.
    :param str line_3: Line 3 on the sign.
    :param str line_4: Line 4 on the sign.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar line_1:
    :ivar line_2:
    :ivar line_3:
    :ivar line_4:
    """

    id = 0x2B
    to = 0

    def __init__(
        self, x: int, y: int, z: int, line_1: str, line_2: str, line_3: str, line_4: str
    ) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.line_1 = line_1
        self.line_2 = line_2
        self.line_3 = line_3
        self.line_4 = line_4

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUpdateSign:
        return cls(
            *buf.unpack_position(),
            buf.unpack_string(),
            buf.unpack_string(),
            buf.unpack_string(),
            buf.unpack_string(),
        )
