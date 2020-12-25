"""Contains animation packets."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayEntityAnimation',)


class PlayEntityAnimation(Packet):
    """Sent whenever an entity should change animation. (Server -> Client)."""

    id_ = 0x05

    def __init__(self, entity_id: int, animation: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.animation = animation

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id) + Buffer.pack('B', self.animation)


class PlayBlockBreakAnimation(Packet):
    """Sent to play a block breaking animation. (Server -> Client)"""

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
