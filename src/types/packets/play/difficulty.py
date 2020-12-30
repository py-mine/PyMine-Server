"""Contains packets related to server difficulty."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayServerDifficulty', 'PlaySetDifficulty',)


class PlayServerDifficulty(Packet):
    """Used by the server to update the difficulty in the client's menu. (Server -> Client)

    :param int difficulty: The difficulty level, see here: https://wiki.vg/Protocol#Server_Difficulty.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr difficulty:
    """

    id = 0x0D
    to = 1

    def __init__(self, difficulty: int) -> None:
        super().__init__()

        self.difficulty = difficulty

    def encode(self) -> bytes:
        return Buffer.pack('B', self.difficulty)


class PlaySetDifficulty(Packet):
    """Used by the client to set difficulty. Not used normally. (Client -> Server)

    :param int new_difficulty: The new difficulty.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr new_difficulty:
    """

    id = 0x02
    to = 0

    def __init__(self, new_difficulty: int) -> None:
        super().__init__()

        self.new_difficulty = new_difficulty

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySetDifficulty:
        return cls(buf.unpack('b'))
