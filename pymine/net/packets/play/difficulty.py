# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar difficulty:
    :ivar locked:
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
