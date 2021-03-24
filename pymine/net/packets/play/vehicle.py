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
            
"""Contains packets related to vehicles and vehicle movement."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayVehicleMoveServerBound",
    "PlayVehicleMoveClientBound",
    "PlaySteerBoat",
    "PlaySteerVehicle",
    "PlaySetPassengers",
)


class PlayVehicleMoveServerBound(Packet):
    """Sent when a player/client moves in a vehicle. (Client -> Server)

    :param float x: The x coordinate of where the player is.
    :param float y: The y coordinate of where the player is.
    :param float z: The z coordinate of where the player is.
    :param float yaw: The yaw (absolute rotation on x axis) in degrees.
    :param float pitch: The pitch (absolute rotation on y axis) in degrees.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar yaw:
    :ivar pitch:
    """

    id = 0x16
    to = 0

    def __init__(self, x: float, y: float, z: float, yaw: float, pitch: float) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.yaw = yaw
        self.pitch = pitch

    @classmethod
    def decode(cls, buf: Buffer) -> PlayVehicleMoveServerBound:
        return cls(buf.unpack("d"), buf.unpack("d"), buf.unpack("d"), buf.unpack("f"), buf.unpack("f"))


class PlayVehicleMoveClientBound(Packet):
    """Sent by the server when a vehicle moves. (Server -> Client)

    :param float x: The x coordinate of where the vehicle is.
    :param float y: The y coordinate of where the vehicle is.
    :param float z: The z coordinate of where the vehicle is.
    :param float yaw: The yaw (absolute rotation on x axis) in degrees.
    :param float pitch: The pitch (absolute rotation on y axis) in degrees.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar yaw:
    :ivar pitch:
    """

    id = 0x2B
    to = 1

    def __init__(self, x: float, y: float, z: float, yaw: float, pitch: float) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.yaw = yaw
        self.pitch = pitch

    def encode(self) -> bytes:
        return (
            Buffer.pack("d", self.x)
            + Buffer.pack("d", self.y)
            + Buffer.pack("d", self.z)
            + Buffer.pack("f", self.yaw)
            + Buffer.pack("f", self.pitch)
        )


class PlaySteerBoat(Packet):
    """Used to visually update when the boat paddles are turning. (Client -> Server)

    :param bool left_paddle_turning: Whether the left paddle is turning or not.
    :param bool right_paddle_turning: Whether the right paddle is turning or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar left_paddle_turning:
    :ivar right_paddle_turning:
    """

    id = 0x17
    to = 0

    def __init__(self, left_paddle_turning: bool, right_paddle_turning: bool) -> None:
        super().__init__()

        self.left_paddle_turning = left_paddle_turning
        self.right_paddle_turning = right_paddle_turning

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySteerBoat:
        return cls(buf.unpack("?"), buf.unpack("?"))


class PlaySteerVehicle(Packet):
    """Sent by the client when movement-related input is sent while on a vehicle. (Client -> Server)

    :param float sideways: Position to the left of the player.
    :param float forward: Positive forward? See here: https://wiki.vg/Protocol#Steer_Vehicle.
    :param int flags: Bit mask: 0x01=jump, 0x02=unmount.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar sideways:
    :ivar forward:
    :ivar flags:
    """

    id = 0x1D
    to = 0

    def __init__(self, sideways: float, forward: float, flags: int) -> None:
        super().__init__()

        self.sideways = sideways
        self.forward = forward
        self.flags = flags

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySteerVehicle:
        return cls(buf.unpack("f"), buf.unpack("f"), buf.unpack("B"))


class PlaySetPassengers(Packet):
    """Sets passengers in a vehicle."""

    id = 0x4B
    to = 1

    def __init__(self, entity_id: int, passenger_count: int, passengers: list) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.passenger_count = passenger_count
        self.passengers = passengers

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_varint(self.passenger_count)
            + b"".join([Buffer.pack_varint(passenger) for passenger in self.passengers])
        )
