"""Contains packets related to scoreboard."""

from __future__ import annotations
import nbt

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ('PlayDisplayScoreboard',)


class PlayDisplayScoreboard(Packet):
    """Insert fancy doscstring here (server -> client)"""

    id = 0x43
    to = 1

    def __init__(self, position: int, score_name: str) -> None:
        super().__init__()

        self.pos = position
        self.score = score_name

    def encode(self) -> bytes:
        return Buffer.pack('b', self.pos) + Buffer.pack_string(self.score)
