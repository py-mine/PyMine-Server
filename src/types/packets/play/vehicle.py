from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayVehicleMoveServerBound', 'PlaySteerBoat')


class PlayVehicleMoveServerBound(Packet):
    """Sent when a player/client moves in a vehicle. (Client -> Server)

    :param float x: The x coordinate of where the player is.
    :param float y: The y coordinate of where the player is.
    :param float z: The z coordinate of where the player is.
    :param float yaw: The yaw (absolute rotation on x axis) in degrees.
    :param float pitch: The pitch (absolute rotation on y axis) in degrees.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr yaw:
    :attr pitch:
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
        return cls(*(buf.unpack('d') for _ in range(5)))


class PlaySteerBoat(Packet):
    """Used to visually update when the boat paddles are turning. (Client -> Server)

    :param bool left_paddle_turning: Whether the left paddle is turning or not.
    :param bool right_paddle_turning: Whether the right paddle is turning or not.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr left_paddle_turning:
    :attr right_paddle_turning:
    """

    id = 0x17
    to = 0

    def __init__(self, left_paddle_turning: bool, right_paddle_turning: bool) -> None:
        super().__init__()

        self.left_paddle_turning = left_paddle_turning
        self.right_paddle_turning = right_paddle_turning

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySteerBoat:
        return cls(buf.unpack_bool(), buf.unpack_bool())
