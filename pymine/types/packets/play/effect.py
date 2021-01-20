"""For packets related to sound and particle effects."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    'PlayEffect',
    'PlayEntityEffect',
)


class PlayEffect(Packet):
    """Used to play a sound or particle effect. (Server -> Client)

    :param int effect_id: The ID of the effect to be played, see here: https://wiki.vg/Protocol#Effect.
    :param int x: The x coordinate where the sound/particle is played.
    :param int y: The y coordinate where the sound/particle is played.
    :param int z: The z coordinate where the sound/particle is played.
    :param int data: Extra data for certain effects.
    :param bool disable_relative_volume: If false, sound effects fade away with distance.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr effect_id:
    :attr x:
    :attr y:
    :attr z:
    :attr data:
    :attr disable_relative_volume:
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
        return Buffer.pack('i', self.effect_id) + Buffer.pack_pos(self.x, self.y, self.z) + Buffer.pack('i', self.data) + \
            Buffer.pack('?', self.disable_relative_volume)


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
