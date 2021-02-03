"""For packets related to sound and particle effects."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayEffect",
    "PlayEntityEffect",
    "PlaySoundEffect",
)


class PlayEffect(Packet):
    """Used to play a sound or particle effect. (Server -> Client)

    :param int effect_id: The ID of the effect to be played, see here: https://wiki.vg/Protocol#Effect.
    :param int x: The x coordinate where the sound/particle is played.
    :param int y: The y coordinate where the sound/particle is played.
    :param int z: The z coordinate where the sound/particle is played.
    :param int data: Extra data for certain effects.
    :param bool disable_relative_volume: If false, sound effects fade away with distance.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar effect_id:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar data:
    :ivar disable_relative_volume:
    """

    id = 0x21
    to = 1

    def __init__(self, effect_id: int, x: int, y: int, z: int, data: int, disable_relative_volume: bool) -> None:
        super().__init__()

        self.effect_id = effect_id
        self.x, self.y, self.z = x, y, z
        self.data = data
        self.disable_relative_volume = disable_relative_volume

    def encode(self) -> bytes:
        return (
            Buffer.pack("i", self.effect_id)
            + Buffer.pack_pos(self.x, self.y, self.z)
            + Buffer.pack("i", self.data)
            + Buffer.pack("?", self.disable_relative_volume)
        )


class PlayEntityEffect(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x59
    to = 1

    def __init__(self, eid: int, effect_id: bytes, amp: bytes, duration: int, flags: bytes) -> None:
        super().__init__()

        self.eid = eid
        self.effect_id = effect_id
        self.amp = amp
        self.duration = duration
        self.flags = flags

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.eid) + self.effect_id + self.amp + Buffer.pack_varint(self.duration) + self.flags


class PlaySoundEffect(Packet):
    """Used to play a hardcoded sound event. (Server -> Client)

    :param int sound_id: The ID of the sound to be played.
    :param int category: The sound category, see here: https://wiki.vg/Protocol#Sound_Effect.
    :param int x: The x coordinate of where the effect is to be played.
    :param int y: The y coordinate of where the effect is to be played.
    :param int z: The z coordinate of where the effect is to be played.
    :param float volume: Volume of the sound to be played, between 0.0 and 1.0.
    :param float pitch: The pitch that the sound should be played at, between 0.5 and 2.0.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar sound_id:
    :ivar category:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar volume:
    :ivar pitch:
    """

    id = 0x51
    to = 1

    def __init__(self, sound_id: int, category: int, x: int, y: int, z: int, volume: float, pitch: float) -> None:
        super().__init__()

        self.sound_id = sound_id
        self.category = category
        self.x, self.y, self.z = x, y, z
        self.volume = volume
        self.pitch = pitch

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.sound_id)
            + Buffer.pack_varint(self.category)
            + Buffer.pack("i", self.x * 8)
            + Buffer.pack("i", self.y * 8)
            + Buffer.pack("i", self.z * 8)
            + Buffer.pack("f", self.volume)
            + Buffer.pack("f", self.pitch)
        )
