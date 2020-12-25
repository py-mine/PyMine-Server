"""Contains animation packets."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayEntityAnimation',)


class PlayEntityAnimation(Packet):
    """Sent whenever an entity should change animation. (Server -> Client)

    :param int entity_id: Entity ID of the digging entity.
    :param int animation: Value 0-5 which correspond to a specific animation (https://wiki.vg/Protocol#Entity_Animation_.28clientbound.29).
    :attr type id_: Unique packet ID.
    :attr entity_id:
    :attr animation:
    """

    id_ = 0x05

    def __init__(self, entity_id: int, animation: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.animation = animation

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id) + Buffer.pack('B', self.animation)


class PlayBlockBreakAnimation(Packet):
    """Sent to play a block breaking animation. (Server -> Client)

    :param int entity_id: Entity ID of the entity which broke the block, or random.
    :param int x: The x coordinate of the location to play the animation.
    :param int y: The y coordinate of the location to play the animation.
    :param int z: The z coordinate of the location to play the animation.
    :param int stage: Stage from 0-9 in the breaking animation.
    :attr type id_: Unique packet ID.
    :attr entity_id:
    :attr x:
    :attr y:
    :attr z:
    :attr stage:

    """

    id_ = 0x08

    def __init__(self, entity_id: int, x: int, y: int, z: int, stage: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.z = z
        self.stage = stage

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id) + \
         Buffer.pack_pos(self.x, self.y, self.z) + \
         Buffer.pack('b', self.stage)
