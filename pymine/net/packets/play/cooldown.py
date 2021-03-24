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
            
"""Contains the PlaySetCooldown packet."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlaySetCooldown",)


class PlaySetCooldown(Packet):
    """Applies a cooldown period to all items with the given type.

    Client bound(Server -> Client)
    :param int item_id: The unique id of the type of affected items.
    :param int cooldown_ticks: The length of the cooldown in in-game ticks.
    :ivar int to: The intended recipient.
    :ivar int id: The unique ID of the packet.
    """

    id = 0x16
    to = 1

    def __init__(self, item_id: int, cooldown_ticks: int) -> None:
        super().__init__()

        self.item_id = item_id
        self.cooldown_ticks = cooldown_ticks

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.item_id) + Buffer.pack_varint(self.cooldown_ticks)
