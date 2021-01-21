"""Contains sound packets."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayNamedSoundEffect",
    "PlayEntitySoundEffect",
)


class PlayNamedSoundEffect(Packet):
    """Used to play a sound effect on the client. Custom sounds may be added by resource packs. Clientbound."""

    id = 0x18
    to = 1

    def __init__(
        self, name: str, category: int, effect_pos_x: int, effect_pos_y: int, effect_pos_z: int, volume: int, pitch: int
    ) -> None:
        super().__init__()

        self.name = name
        self.category = category
        self.effect_pos_x = effect_pos_x
        self.effect_pos_y = effect_pos_y
        self.effect_pos_z = effect_pos_z
        self.volume = volume
        self.pitch = pitch

    def encode(self) -> bytes:
        return (
            Buffer.pack_string(self.name)
            + Buffer.pack_varint(self.category)
            + Buffer.pack("i", self.category)
            + Buffer.pack("i", self.effect_pos_x)
            + Buffer.pack("i", self.effect_pos_y)
            + Buffer.pack("i", self.effect_pos_z)
            + Buffer.pack("f", self.volume)
            + Buffer.pack("f", self.pitch)
        )


class PlayEntitySoundEffect(Packet):
    """Insert fancy Docstring here (server -> client)"""

    id = 0x50
    to = 1

    def __init__(self, sound_id: int, category: int, eid: int, volume: float, pitch: float) -> None:
        super().__init__()

        self.sound_id = sound_id
        self.category = category
        self.eid = eid
        self.volume = volume
        self.pitch = pitch

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.sound_id)
            + Buffer.pack_varint(self.category)
            + Buffer.pack_varint(self.eid)
            + Buffer.pack("f", self.volume)
            + Buffer.pack("f", self.pitch)
        )
