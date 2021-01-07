"""Contains packets related to beacons."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlaySetBeaconEffect',)


class PlaySetBeaconEffect(Packet):
    """Changes the effect of the current beacon. (Client -> Server)

    :param int primary_effect: Description of parameter `primary_effect`.
    :param int secondary_effect: Description of parameter `secondary_effect`.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr primary_effect:
    :attr secondary_effect:
    """

    id = 0x24
    to = 0

    def __init__(self, primary_effect: int, secondary_effect: int) -> None:
        super().__init__()

        self.primary_effect = primary_effect
        self.secondary_effect = secondary_effect

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySetBeaconEffect:
        return cls(buf.unpack_varint(), buf.unpack_varint())
