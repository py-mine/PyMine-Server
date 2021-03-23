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
"""Contains packets related to advancements."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayAdvancementTab",
    "PlaySelectAdvancementTab",
)


class PlayAdvancementTab(Packet):
    """Related to advancement tab menu, see here: https://wiki.vg/Protocol#Advancement_Tab (Client -> Server)

    :param int action: Either opened tab (0), or closed screen (1).
    :param int tab_id: The ID of the tab, only present if action is 0 (opened tab)
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar action:
    :ivar tab_id:
    """

    id = 0x22
    to = 0

    def __init__(self, action: int, tab_id: int) -> None:
        super().__init__()

        self.action = action
        self.tab_id = tab_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayAdvancementTab:
        return cls(buf.unpack_varint(), buf.unpack_optional(buf.unpack_varint))


class PlaySelectAdvancementTab(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x3C
    to = 1

    def __init__(self, identifier: str = None) -> None:
        super().__init__()

        self.identifier = identifier

    def encode(self) -> bytes:
        return Buffer.pack_optional(Buffer.pack_string, self.identifier)
