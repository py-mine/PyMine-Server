"""Contains the PlaySetCooldown packet"""
from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlaySetCooldown',)


class PlaySetCooldown(Packet):
    """Applies a cooldown period to all items with the given type."""
    id = 0x16
    to = 1

    def __init__(self, item_id: int, cooldown_ticks: int):
        self.item_id = item_id
        self.cooldown_ticks = cooldown_ticks

    def encode(self):
        return Buffer.pack_varint(self.item_id) + Buffer.pack_varint(self.cooldown_ticks)
