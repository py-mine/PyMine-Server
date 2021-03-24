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
            
"""Contains statistics packet."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayStatistics",)


class PlayStatistics(Packet):
    """Send data in the stats menu to client. (Server -> Client)

    :param list stats: A list of stat entries (see here: https://wiki.vg/Protocol#Statistics).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar stats:
    """

    id = 0x06
    to = 1

    def __init__(self, stats: list) -> None:
        super().__init__()

        self.stats = stats

        # Stats should be a list like:
        # [
        #     [category_id: int, statistic_id: int, value: int],
        #     ...
        # ]

    def encode(self) -> bytes:
        out = Buffer.pack_varint(len(self.stats))

        for entry in self.stats:
            out += b"".join([Buffer.pack_varint(e) for e in entry])

        return out
