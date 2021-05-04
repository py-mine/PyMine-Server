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

"""Contains packets related to the in-game map item."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chat import Chat

__all__ = ("PlayMapData",)


class PlayMapData(Packet):
    """Insert fancy shmancy docstring"""

    id = 0x25
    to = 1

    def __init__(
        self,
        map_id: int,
        scale: int,
        tracking_pos: bool,
        locked: bool,
        icons: list,
        cols: int,
        rows: int = None,
        x: int = None,
        z: int = None,
        data: bytes = None,
    ) -> None:
        super().__init__()

        self.map_id = map_id
        self.scale = scale
        self.tracking_pos = tracking_pos
        self.locked = locked
        self.icons = icons
        self.cols = cols
        self.rows = rows
        self.x, self.z = x, z
        self.data = data

    def encode(self) -> bytes:
        out = (
            Buffer.pack_varint(self.map_id)
            + Buffer.pack("b", self.scale)
            + Buffer.pack("?", self.tracking_pos)
            + Buffer.pack("?", self.locked)
            + Buffer.pack_varint(len(self.icons))
        )

        for icon in self.icons:
            out += Buffer.pack_varint(icon["type"]) + Buffer.pack("b", icon["x"]) + Buffer.pack("b", icon["z"])

            display_name = icon.get("display_name")

            if display_name is not None:
                out += Buffer.pack("?", True) + Buffer.pack_chat(Chat(display_name))
            else:
                out += Buffer.pack("?", False)

        out += (
            Buffer.pack("B", self.cols)
            + Buffer.pack_optional((lambda x: Buffer.pack("B", x)), self.rows)
            + Buffer.pack_optional((lambda x: Buffer.pack("b", x)), self.x)
            + Buffer.pack_optional((lambda z: Buffer.pack("b", z)), self.z)
        )

        if self.data is not None:
            out += Buffer.pack("?", True) + Buffer.pack_varint(len(self.data)) + Buffer.pack("?", True) + self.data
        else:
            out += Buffer.pack("?", False) + Buffer.pack("?", False)

        return out
