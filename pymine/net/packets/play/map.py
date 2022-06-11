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
    """Updates a rectangular area on a map item. (Server -> Client)

    :param int map_id: Map ID of the map being modified.
    :param int scale: Value from 0 (1x1 blocks per pixel) to 4 (16x16 blocks per pixel).
    :param bool tracking_pos: Specifies whether player and item frame icons are shown.
    :param bool locked: True if the map has been locked in a cartography table.
    :param list icons: List. Elements (in order):
     - Type (int): Type of icon.
     - X (int): Map coordinates: -128 for furthest left, +127 for furthest right.
     - Z (int): Map coordinates: -128 for highest, +127 for lowest.
     - Direction (int): 0-15. 0 is a vertical icon and increments by 22.5° (360/16).
     - HasDisplayName (bool): Does the icon have a display name?
     - DisplayName (optional, Chat): Only present if previous bool is True. Icon's display name.
    :param int cols: Number of columns updated.
    :param int rows: Only if Columns is more than 0; number of rows updated.
    :param int x: Only if Columns is more than 0; x offset of the westernmost column.
    :param int z: Only if Columns is more than 0; z offset of the northernmost row.
    :param bytes data: Only if Columns is more than 0; map item data.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar map_id:
    :ivar scale:
    :ivar tracking_pos:
    :ivar locked:
    :ivar icons:
    :ivar cols:
    :ivar rows:
    :ivar x:
    :ivar z:
    :ivar data:
    """

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
            out += (
                Buffer.pack_varint(icon["type"])
                + Buffer.pack("b", icon["x"])
                + Buffer.pack("b", icon["z"])
            )

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
            out += (
                Buffer.pack("?", True)
                + Buffer.pack_varint(len(self.data))
                + Buffer.pack("?", True)
                + self.data
            )
        else:
            out += Buffer.pack("?", False) + Buffer.pack("?", False)

        return out
