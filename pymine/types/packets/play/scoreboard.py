"""Contains packets related to scoreboard."""

from __future__ import annotations
import nbt

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayDisplayScoreboard",
    "PlayUpdateScore",
)


class PlayDisplayScoreboard(Packet):
    """Insert fancy doscstring here (server -> client)"""

    id = 0x43
    to = 1

    def __init__(self, position: int, score_name: str) -> None:
        super().__init__()

        self.pos = position
        self.score = score_name

    def encode(self) -> bytes:
        return Buffer.pack("b", self.pos) + Buffer.pack_string(self.score)


class PlayUpdateScore(Packet):
    """Insert fancy doscstring here (server -> client)"""

    id = 0x4D
    to = 1

    def __init__(self, entity_name: str, action: bytes, objective_name: str, value: int) -> None:
        super().__init__()

        self.entity_name = entity_name
        self.action = action
        self.objective_name = objective_name
        self.value = value

    def encode(self) -> bytes:
        return (
            Buffer.pack_string(self.entity_name)
            + self.action
            + Buffer.pack_string(self.objective_name)
            + Buffer.pack_optional_varint(self.value)
        )
