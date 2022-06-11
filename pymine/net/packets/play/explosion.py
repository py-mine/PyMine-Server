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

"""Contains packets related to entities."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayExplosion",)


class PlayExplosion(Packet):
    """Sent when an explosion occurs (creepers, TNT, and ghast fireballs). (Server -> Client)

    :param int x: Explosion X coordinate
    :param int y: Explosion Y coordinate
    :param int z: Explosion Z coordinate
    :param int strength: Explosion strength.
    :param int record_count: Number of elements in the following array. FIXME: This is not needed.
    :param list records: Affected blocks.
    :param int pmx: X velocity of the player being pushed by the explosion.
    :param int pmy: Y velocity of the player being pushed by the explosion.
    :param int pmz: Z velocity of the player being pushed by the explosion.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar strength:
    :ivar record_count:
    :ivar records:
    :ivar pmx:
    :ivar pmy:
    :ivar pmz:
    """

    id = 0x1B
    to = 1

    def __init__(
        self,
        x: int,
        y: int,
        z: int,
        strength: int,
        record_count: int,
        records: list,
        pmx: int,
        pmy: int,
        pmz: int,
    ) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.strength = strength
        self.record_count = record_count
        self.records = records
        self.pmx = pmx
        self.pmy = pmy
        self.pmz = pmz

    def encode(self) -> bytes:
        return (
            Buffer.pack("f", self.x)
            + Buffer.pack("f", self.y)
            + Buffer.pack("f", self.z)
            + Buffer.pack("f", self.strength)
            + Buffer.pack("i", self.record_count)
            + b"".join([Buffer.pack("b", r) for r in self.records])
            + Buffer.pack("f", self.pmx)
            + Buffer.pack("f", self.pmy)
            + Buffer.pack("f", self.pmz)
        )
