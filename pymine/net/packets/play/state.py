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

"""Contains packets related to game state."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayChangeGameState",)


class PlayChangeGameState(Packet):
    """Used for weather, bed use, gamemode and demo messages. (Server -> Client)

    :param int reason: Reason code.
    :param float value: Reason value. Depends on reason.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar reason:
    :ivar value:
    """

    id = 0x1D
    to = 1

    def __init__(self, reason: int, value: float) -> None:
        super().__init__()

        self.reason = reason
        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("B", self.reason) + Buffer.pack("f", self.value)
