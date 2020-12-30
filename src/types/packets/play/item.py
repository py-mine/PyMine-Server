"""Contains packets related to items."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayUseItem',)


class PlayUseItem(Packet):
    """Short summary.

    :param int hand: The hand used for the animation. main hand (0) or offhand (1).
    :attr type id: Unique packet ID.
    :attr type to: Packet direction.
    :attr hand:
    """

    id = 0x2F
    to = 0

    def __init__(self, hand: int) -> None:
        super().__init__()

        self.hand = hand

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUseItem:
        return cls(buf.upack_varint())
