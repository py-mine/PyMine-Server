"""Contains sound packets."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayNamedSoundEffect',)


class PlayNamedSoundEffect(Packet):
    """Used to play a sound effect on the client. Custom sounds may be added by resource packs. Clientbound."""
    id = 0x18
    to = 1

    def __init__(self, name: str, category: int, effect_pos_x: int, effect_pos_y: int, effect_pos_z: int, volume: int, pitch: int):
        self.name = name
        self.category = category
        self.effect_pos_x = effect_pos_x
        self.effect_pos_y = effect_pos_y
        self.effect_pos_z = effect_pos_z
        self.volume = volume
        self.pitch = pitch

    def encode(self):
        return Buffer.pack_string(self.name) + Buffer.pack_varint(self.category) + Buffer.pack('i', self.category) + Buffer.pack('i', self.effect_pos_x) + Buffer.pack('i', self.effect_pos_y) + Buffer.pack('i', self.effect_pos_z + Buffer.pack('f', self.volume) + Buffer.pack('f', self.pitch)
