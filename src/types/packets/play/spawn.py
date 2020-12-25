"""Contains spawn packets."""

from __future__ import annotations
import uuid

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = (
    'PlayEntitySpawn',
    'PlayLivingEntitySpawn',
    'PlayPaintingSpawn',
    'PlaySpawnExperienceOrb',
)


class PlayEntitySpawn(Packet):
    """Sent by the server when a vehicle or other non-living entity is created. Client bound(Server -> Client)."""

    id_ = 0x00

    def __init__(self, entity_id: int, object_uuid: uuid.UUID, type: int,
                 x: int, y: int, z: int, pitch: int, yaw: int, data: int,
                 vloc_x: int, vloc_y: int, vloc_z: int) -> None:
        super().__init__()
        self.entity_id = entity_id
        self.object_uuid = object_uuid
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.data = data
        self.vloc_x = vloc_x
        self.vloc_y = vloc_y
        self.vloc_z = vloc_z

    def encode(self):
        return Buffer.pack_varint(self.entity_id) + Buffer.pack_uuid(self.object_uuid) + Buffer.pack_varint(self.type) + Buffer.pack('d' + self.x) + Buffer.pack('d' + self.y) + Buffer.pack(
            'd' + self.z) + Buffer.pack('i' + self.pitch) + Buffer.pack('i' + self.yaw) + Buffer.pack('h' + self.vloc_x) + Buffer.pack('h' + self.vloc_x) + Buffer.pack('h' + self.vloc_z)


class PlaySpawnExperienceOrb(Packet):
    """Spawns one or more experience orbs. Client bound(Server -> Client)."""

    id_ = 0x01

    def __init__(self, entity_id: int, x: int = 0, y: int = 0, z: int = 0, count: int = 1237) -> None:  # nopep8
        super().__init__()
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z
        self.count = count

    def encode(self):
        return Buffer.pack_varint(self.entity_id) + Buffer.pack('d', self.x) + \
            Buffer.pack('d', self.y) + Buffer.pack('d', self.z) + \
            Buffer.pack('h', self.count)


class PlayLivingEntitySpawn(Packet):
    """Sent by the server when a living entity is spawned.  Client bound(Server -> Client)."""

    id_ = 0x02

    def __init__(self, entity_id: int, object_uuid: uuid.UUID, type: int,
                 x: int, y: int, z: int, pitch: int, head_pitch: int, yaw: int,
                 vloc_x: int, vloc_y: int, vloc_z: int) -> None:
        super().__init__()
        self.entity_id = entity_id
        self.object_uuid = object_uuid
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.head_pitch = head_pitch
        self.vloc_x = vloc_x
        self.vloc_y = vloc_y
        self.vloc_z = vloc_z

    def encode(self):
        return Buffer.pack_varint(self.entity_id) + Buffer.pack_uuid(self.object_uuid) + Buffer.pack_varint(self.type) + Buffer.pack('d' + self.x) + Buffer.pack('d' + self.y) + Buffer.pack(
            'd' + self.z) + Buffer.pack('i' + self.pitch) + Buffer.pack('i' + self.yaw) + Buffer.pack('i', self.head_pitch) + Buffer.pack('h' + self.vloc_x) + Buffer.pack('h' + self.vloc_x) + Buffer.pack('h' + self.vloc_z)


class PlayPaintingSpawn(Packet):
    """This packet shows location, name, and type of painting.  Client bound(Server -> Client)."""

    id_ = 0x03

    def __init__(self, entity_id: int, entity_uuid: uuid.UUID, motive: int, location: int, direction: int) -> None:
        super().__init__()
        self.entity_id = entity_id
        self.entity_uuid = entity_uuid
        self.motive = motive
        self.location = location
        self.direction = direction

    def encode(self):
        return Buffer.pack_varint(self.entity_id) + Buffer.pack_uuid(self.entity_uuid) + \
            Buffer.pack_varint(self.motive) + Buffer.pack_pos(self.location) + \
            Buffer.pack('i', self.direction)
