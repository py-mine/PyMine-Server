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

"""Contains packets related to scoreboard."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chat import Chat
import pymine.types.nbt as nbt

__all__ = (
    "PlayDisplayScoreboard",
    "PlayUpdateScore",
    "PlayScoreboardObjective",
)


class PlayDisplayScoreboard(Packet):
    """Ssent to the client when it should display a scoreboard. (Server -> Client)

    :param int position: The position of the scoreboard.
     - 0: list
     - 1: sidebar
     - 2: below name
     - 3-18: team specific sidebar, indexed as 3 + team color.
    :param str score_name: The unique name for the scoreboard to be displayed.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar position:
    :ivar score_name:
    """

    id = 0x43
    to = 1

    def __init__(self, position: int, score_name: str) -> None:
        super().__init__()

        self.pos = position
        self.score = score_name

    def encode(self) -> bytes:
        return Buffer.pack("b", self.pos) + Buffer.pack_string(self.score)


class PlayUpdateScore(Packet):
    """Sent to the client when it should update a scoreboard item. (Server -> Client)

    :param str entity_name: The entity whose score this is.
     - For players, this is their username
     - For other entities, it is their UUID.
    :param bytes action: 0 to create/update an item. 1 to remove an item.
    :param str objective_name: The name of the objective the score belongs to.
    :param int value: The score to be displayed next to the entry. Only sent when action == 0.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_name:
    :ivar action:
    :ivar objective_name:
    :ivar value:
    """

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
    """Sent when it should create a new scoreboard objective or remove one. (Server -> Client)

    :param str objective_name: The unique objective name.
    :param int mode: Either create (0), remove (1), or edit (2)
    :param str objective_value: The value to put in.
    :param int type_: Either integer (0), or hearts (1)
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar objective_name:
    :ivar mode:
    :ivar objective_value:
    :ivar type_:
    """

    id = 0x4A
    to = 1

    def __init__(
        self, objective_name: str, mode: int, value: str = None, type_: int = None
    ) -> None:
        super().__init__()

        self.objective_name = objective_name
        self.mode = mode
        self.value = value
        self.type_ = type_

    def encode(self) -> bytes:
        return (
            Buffer.pack_string(self.objective_name)
            + Buffer.pack("b", self.mode)
            + Buffer.pack_optional(Buffer.pack_chat, Chat(self.objective_value))
            + Buffer.pack_optional(Buffer.pack_varint, self.type_)
        )
