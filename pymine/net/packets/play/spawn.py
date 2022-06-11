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

"""Contains spawn packets."""

from __future__ import annotations

import uuid

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayEntitySpawn",
    "PlayLivingEntitySpawn",
    "PlayPaintingSpawn",
    "PlaySpawnExperienceOrb",
    "PlaySpawnPlayer",
    "PlaySpawnPosition",
)


class PlayEntitySpawn(Packet):
    """Sent by the server when a vehicle or other non-living entity is created. (Server -> Client).

    :param int entity_id: The Entity ID.
    :param uuid.UUID object_uuid: Object UUID.
    :param int type_: The type of entity.
    :param int x: X coordinate.
    :param int y: Y coordinate.
    :param int z: Z coordinate.
    :param int pitch: Entity pitch.
    :param int yaw: Entity yaw.
    :param int data: Meaning dependent on the value of the type_ field.
    :param int vloc_x: Entity X velocity.
    :param int vloc_y: Entity Y velocity.
    :param int vloc_z: Entity Z velocity.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar object_uuid:
    :ivar type_:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar pitch:
    :ivar yaw:
    :ivar data:
    :ivar vloc_x:
    :ivar vloc_y:
    :ivar vloc_z:
    """

    id = 0x00
    to = 1

    def __init__(
        self,
        entity_id: int,
        object_uuid: uuid.UUID,
        type_: int,
        x: int,
        y: int,
        z: int,
        pitch: int,
        yaw: int,
        data: int,
        vloc_x: int,
        vloc_y: int,
        vloc_z: int,
    ) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.object_uuid = object_uuid
        self.type_ = type_
        self.x, self.y, self.z = x, y, z
        self.pitch = pitch
        self.yaw = yaw
        self.data = data
        self.vloc_x = vloc_x
        self.vloc_y = vloc_y
        self.vloc_z = vloc_z

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_uuid(self.object_uuid)
            + Buffer.pack_varint(self.type_)
            + Buffer.pack("d" + self.x)
            + Buffer.pack("d" + self.y)
            + Buffer.pack("d" + self.z)
            + Buffer.pack("i" + self.pitch)
            + Buffer.pack("i" + self.yaw)
            + Buffer.pack("h" + self.vloc_x)
            + Buffer.pack("h" + self.vloc_x)
            + Buffer.pack("h" + self.vloc_z)
        )


class PlaySpawnExperienceOrb(Packet):
    """Spawns one or more experience orbs. (Server -> Client)

    :param int entity_id: The Entity ID.
    :param int x: X coordinate of the experience orb.
    :param int y: Y coordinate of the experience orb.
    :param int z: Z coordinate of the experience orb.
    :param int count: The amount of experience this orb will reward once collected.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar count:
    """

    id = 0x01
    to = 1

    def __init__(
        self, entity_id: int, x: int = 0, y: int = 0, z: int = 0, count: int = 1237
    ) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.x, self.y, self.z = x, y, z
        self.count = count

    def encode(self):
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack("d", self.x)
            + Buffer.pack("d", self.y)
            + Buffer.pack("d", self.z)
            + Buffer.pack("h", self.count)
        )


class PlayLivingEntitySpawn(Packet):
    """Sent by the server when a living entity is spawned. (Server -> Client)

    :param int entity_id: The Entity ID.
    :param uuid.UUID object_uuid: Object UUID.
    :param int type_: The type of entity.
    :param int x: X coordinate.
    :param int y: Y coordinate.
    :param int z: Z coordinate.
    :param int pitch: Entity pitch.
    :param int head_pitch: Entity head pitch.
    :param int yaw: Entity yaw.
    :param int vloc_x: Entity X velocity.
    :param int vloc_y: Entity Y velocity.
    :param int vloc_z: Entity Z velocity.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar object_uuid:
    :ivar type_:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar pitch:
    :ivar yaw:
    :ivar head_pitch:
    :ivar vloc_x:
    :ivar vloc_y:
    :ivar vloc_z:
    """

    id = 0x02
    to = 1

    def __init__(
        self,
        entity_id: int,
        object_uuid: uuid.UUID,
        type_: int,
        x: int,
        y: int,
        z: int,
        pitch: int,
        head_pitch: int,
        yaw: int,
        vloc_x: int,
        vloc_y: int,
        vloc_z: int,
    ) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.object_uuid = object_uuid
        self.type_ = type_
        self.x, self.y, self.z = x, y, z
        self.pitch = pitch
        self.yaw = yaw
        self.head_pitch = head_pitch
        self.vloc_x = vloc_x
        self.vloc_y = vloc_y
        self.vloc_z = vloc_z

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_uuid(self.object_uuid)
            + Buffer.pack_varint(self.type_)
            + Buffer.pack("d" + self.x)
            + Buffer.pack("d" + self.y)
            + Buffer.pack("d" + self.z)
            + Buffer.pack("i" + self.pitch)
            + Buffer.pack("i" + self.yaw)
            + Buffer.pack("i", self.head_pitch)
            + Buffer.pack("h" + self.vloc_x)
            + Buffer.pack("h" + self.vloc_x)
            + Buffer.pack("h" + self.vloc_z)
        )


class PlayPaintingSpawn(Packet):
    """This packet shows location, name, and type of painting. (Server -> Client)

    :param int entity_id: The Entity ID.
    :param uuid.UUID entity_uuid: Entity UUID.
    :param int motive: Painting's ID, see below.
    :param int location: Center coordinates (see below).
    :param int direction: Direction the painting faces (South = 0, West = 1, North = 2, East = 3).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar entity_uuid:
    :ivar motive:
    :ivar location:
    :ivar direction:
    """

    id = 0x03
    to = 1

    def __init__(
        self, entity_id: int, entity_uuid: uuid.UUID, motive: int, location: int, direction: int
    ) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.entity_uuid = entity_uuid
        self.motive = motive
        self.location = location
        self.direction = direction

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_uuid(self.entity_uuid)
            + Buffer.pack_varint(self.motive)
            + Buffer.pack_position(self.location)
            + Buffer.pack("b", self.direction)
        )


class PlaySpawnPlayer(Packet):
    """Sent by the server when a player comes into visible range. (Server -> Client)

    :param int entity_id: Player's Entity ID.
    :param uuid.UUID player_uuid: Player UUID.
    :param int x: Player X coordinate.
    :param int y: Player Y coordinate.
    :param int z: Player Z coordinate.
    :param int pitch: Player pitch.
    :param int yaw: Player yaw.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar player_uuid:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar pitch:
    :ivar yaw:
    """

    id = 0x04
    to = 1

    def __init__(
        self, entity_id: int, player_uuid: uuid.UUID, x: int, y: int, z: int, pitch: int, yaw: int
    ) -> None:
        super.__init__()

        self.entity_id = entity_id
        self.player_uuid = player_uuid
        self.x, self.y, self.z = x, y, z
        self.pitch, self.yaw = pitch, yaw

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_uuid(self.player_uuid)
            + Buffer.pack("d", self.x)
            + Buffer.pack("d", self.y)
            + Buffer.pack("d", self.z)
            + Buffer.pack("B", self.pitch)
            + Buffer.pack("B", self.yaw)
        )


class PlaySpawnPosition(Packet):
    """Sent after login to specify the coordinates of the spawn point. (Server -> Client)

    :param int x: Spawn point X coordinate.
    :param int y: Spawn point Y coordinate.
    :param int z: Spawn point Z coordinate.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    """

    id = 0x42
    to = 1

    def __init__(self, x: int, y: int, z: int) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z

    def encode(self) -> bytes:
        return Buffer.pack_position(self.x, self.y, self.z)
