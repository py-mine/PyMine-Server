"""Contains packets related to scoreboard."""

from __future__ import annotations
import nbt

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chat import Chat

__all__ = (
    "PlayDisplayScoreboard",
    "PlayUpdateScore",
    "PlayScoreboardObjective",
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


class PlayScoreboardObjective(Packet):
    """Sent to the client when it should create a new scoreboard objective or remove one. (Server -> Client)

    :param str objective_name: The unique objective name.
    :param int mode: Either create (0), remove (1), or edit (2)
    :param str objective_value: The value to put in.
    :param int type_: Either integer (0), or hearts (1)
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr objective_name:
    :attr mode:
    :attr objective_value:
    :attr type_:
    """

    id = 0x4A
    to = 1

    def __init__(self, objective_name: str, mode: int, value: str = None, type_: int = None) -> None:
        super().__init__()

        self.objective_name = objective_name
        self.mode = mode
        self.value = value
        self.type_ = type_

    def encode(self) -> bytes:
        out = (
            Buffer.pack_string(self.objective_name)
            + Buffer.pack("b", self.mode)
            + Buffer.pack_optional(Buffer.pack_chat, Chat(self.objective_value))
            + Buffer.pack_optional(Buffer.pack_varint, self.type_)
        )
