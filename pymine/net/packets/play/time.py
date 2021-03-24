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
            
"""Contains packets related to time."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayUpdateTime",)


class PlayUpdateTime(Packet):
    """Updates time.

    :param int world_age: In ticks, not changed by server commands.
    :param int day_time: The world (or region) time, in ticks. If negative the sun will stop moving at the Math.abs of the time.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar int world_age:
    :ivar int day_time:
    """

    id = 0x4E
    to = 1

    def __init__(self, world_age: int, day_time: int) -> None:
        super().__init__()

        self.world_age = world_age
        self.day_time = day_time

    def encode(self) -> bytes:
        return Buffer.pack("l", self.world_age) + Buffer.pack("l", self.day_time)
