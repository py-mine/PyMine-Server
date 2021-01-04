"""Contains packets related to potions and effects."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('',)


class PlayEffect(Packet):

    id = 0x21
    to = 1

    def __init__(
            self,
            effect_id: int,
            x: int,
            y: int,
            z: int,
            data: int,
            disable_relative_volume: bool) -> None:
        raise NotImplementedError

    def encode(self) -> bytes:
        raise NotImplementedError
