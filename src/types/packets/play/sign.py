"""Contains packets related to signs."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayUpdateSign',)


class PlayUpdateSign(Packet):
    """Short summary.

    :param int x: The x coordinate of the sign.
    :param int y: The y coordinate of the sign.
    :param int z: The z coordinate of the sign.
    :param str line_1: Line 1 on the sign.
    :param str line_2: Line 2 on the sign.
    :param str line_3: Line 3 on the sign.
    :param str line_4: Line 4 on the sign.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr line_1:
    :attr line_2:
    :attr line_3:
    :attr line_4:
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
        return cls(
            *buf.unpack_pos(),
            buf.unpack_string(),
            buf.unpack_string(),
            buf.unpack_string(),
            buf.unpack_string()
        )
