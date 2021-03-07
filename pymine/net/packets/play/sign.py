"""Contains packets related to signs."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayUpdateSign",)


class PlayUpdateSign(Packet):
    """Sent from the client when the done button is pressed in the sign GUI. (Client -> Server)

    :param int x: The x coordinate of the sign.
    :param int y: The y coordinate of the sign.
    :param int z: The z coordinate of the sign.
    :param str line_1: Line 1 on the sign.
    :param str line_2: Line 2 on the sign.
    :param str line_3: Line 3 on the sign.
    :param str line_4: Line 4 on the sign.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar line_1:
    :ivar line_2:
    :ivar line_3:
    :ivar line_4:
    """

    id = 0x2B
    to = 0

    def __init__(self, x: int, y: int, z: int, line_1: str, line_2: str, line_3: str, line_4: str) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.line_1 = line_1
        self.line_2 = line_2
        self.line_3 = line_3
        self.line_4 = line_4

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUpdateSign:
        return cls(*buf.unpack_position(), buf.unpack_string(), buf.unpack_string(), buf.unpack_string(), buf.unpack_string())
