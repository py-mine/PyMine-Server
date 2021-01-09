"""Contains packets related to time."""
from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer


class PlayUpdateLight(Packet):
    """Updates time.

    :param int world_age: In ticks, not changed by server commands.
    :param int day_time: The world (or region) time, in ticks. If negative the sun will stop moving at the Math.abs of the time.
    :attr int world_age:
    :attr int day_time:
    """

    id = 0x4E
    to = 1

    def __init__(self, world_age: int, day_time: int) -> None:
        self.world_age = world_age
        self.day_time = day_time

    def encode(self) -> bytes:
        return Buffer.pack('l', self.world_age) + Buffer.pack('l', self.day_time)
