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

from __future__ import annotations

from pymine.types.buffer import Buffer
from pymine.types.packet import Packet

__all__ = (
    "StatusStatusRequest",
    "StatusStatusResponse",
    "StatusStatusPingPong",
)


class StatusStatusRequest(Packet):
    """Request from the client to get information on the server. (Client -> Server)

    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    """

    id = 0x00
    to = 0

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def decode(cls, buf: Buffer) -> StatusStatusRequest:
        return cls()


class StatusStatusResponse(Packet):
    """Returns server status data back to the requesting client. (Server -> Client)

    :param dict response_data: JSON response data sent back to the client.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar response_data:
    """

    id = 0x00
    to = 1

    def __init__(self, response_data: dict) -> None:
        # What response_data should be like
        # {
        #     "version": {
        #         "name": "1.8.7",
        #         "protocol": 47
        #     },
        #     "players": {
        #         "max": 100,
        #         "online": 5,
        #         "sample": [
        #             {
        #                 "name": "thinkofdeath",
        #                 "id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20"
        #             }
        #         ]
        #     },
        #     "description": {  # a Chat
        #         "text": "Hello world"
        #     },
        #     "favicon": "data:image/png;base64,<data>"
        # }

        super().__init__()

        self.response_data = response_data

    def encode(self) -> bytes:
        return Buffer.pack_json(self.response_data)


class StatusStatusPingPong(Packet):
    """Ping pong? (Server -> Client AND Client -> Server)

    :param int payload: A long number, randomly generated or what the client sent.
    :ivar int id: Unique packet ID.
    :ivar int payload:
    """

    id = 0x01
    to = 2

    def __init__(self, payload: int) -> None:
        super().__init__()

        self.payload = payload

    @classmethod
    def decode(cls, buf: Buffer) -> StatusStatusPingPong:
        return cls(buf.unpack("q"))

    def encode(self) -> bytes:
        return Buffer.pack("q", self.payload)
