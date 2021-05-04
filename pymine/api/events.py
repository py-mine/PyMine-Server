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

from pymine.types.abc import AbstractEvent


class GenericEvent(AbstractEvent):
    """Used to create events which take no extra parameters."""

    def __init__(self, handler):
        self.handler = handler


class PacketEvent(AbstractEvent):
    """Triggered when an oncoming packet for the specified state id and packet id is received."""

    def __init__(self, handler, state_id: int, packet_id: int):
        self.handler = handler
        self.state_id = state_id
        self.packet_id = packet_id


class ServerStartEvent(GenericEvent):
    """Triggered when the server starts up."""


class ServerStopEvent(GenericEvent):
    """Triggered when the server shuts down, before each plugin cog is teared down."""
