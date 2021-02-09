"""Contains sound packets."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayNamedSoundEffect",
    "PlayEntitySoundEffect",
    "PlayStopSound",
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


class PlayStopSound(Packet):
    """Sent by the server to stop a sound. (Server -> Client)

    :param int flags: Tells what data is going to be sent.
    :param int source: See here: https://wiki.vg/Protocol#Stop_Sound.
    :param str sound: See here: https://wiki.vg/Protocol#Stop_Sound.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar flags:
    :ivar source:
    :ivar sound:
    """

    id = 0x52
    to = 1

    def __init__(self, flags: int, source: int = None, sound: str = None) -> None:
        super().__init__()

        self.flags = flags
        self.source = source
        self.sound = sound

    def encode(self) -> bytes:
        return (
            Buffer.pack("b", self.flags)
            + Buffer.pack_optional(Buffer.pack_varint, self.source)
            + Buffer.pack_optional(Buffer.pack_string, self.sound)
        )
