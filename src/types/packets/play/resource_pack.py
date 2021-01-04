"""Contains packets related to resource packs."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayResourcePackStatus',)


class PlayResourcePackStatus(Packet):
    """Used by the client to send the status of whether a resource pack was loaded or not. (Client -> Server)

    :param int status: One of: successfully loaded (0), declined (1), failed download (2), accepted (3).
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr status:
    """

    id = 0x21
    to = 0

    def __init__(self, status: int) -> None:
        super().__init__()

        self.status = status

    @classmethod
    def decode(cls, buf: Buffer) -> PlayResourcePackStatus:
        return cls(buf.unpack_varint())
