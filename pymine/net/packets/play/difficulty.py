"""Contains packets related to server difficulty."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayServerDifficulty",
    "PlaySetDifficulty",
    "PlayLockDifficulty",
)


class PlayServerDifficulty(Packet):
    """Used by the server to update the difficulty in the client's menu. (Server -> Client)

    :param int difficulty: The difficulty level, see here: https://wiki.vg/Protocol#Server_Difficulty.
    :param bool locked: Whether the difficulty is locked or not.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr difficulty:
    :attr locked:
    """

    id = 0x0D
    to = 1

    def __init__(self, difficulty: int, locked: bool) -> None:
        super().__init__()

        self.difficulty = difficulty
        self.locked = locked

    def encode(self) -> bytes:
        return Buffer.pack("B", self.difficulty) + Buffer.pack("?", self.locked)


class PlaySetDifficulty(Packet):
    """Used by the client to set difficulty. Not used normally. (Client -> Server)

    :param int new_difficulty: The new difficulty.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar new_difficulty:
    """

    id = 0x02
    to = 0

    def __init__(self, new_difficulty: int) -> None:
        super().__init__()

        self.new_difficulty = new_difficulty

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySetDifficulty:
        return cls(buf.unpack("b"))


class PlayLockDifficulty(Packet):
    """Used to lock the difficulty. Only used on singleplayer. (Client -> Server)

    :param bool locked: Whether the difficulty is locked or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar locked:
    """

    id = 0x11
    to = 0

    def __init__(self, locked: bool) -> None:
        super().__init__()

        self.locked = locked

    @classmethod
    def decode(cls, buf: Buffer) -> PlayLockDifficulty:
        return cls(buf.unpack("?"))
