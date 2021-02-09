"""Contains LoginSetCompression which is technically part of the login process."""

from __future__ import annotations

from pymine.types.buffer import Buffer
from pymine.types.packet import Packet

__all__ = ("LoginSetCompression",)


class LoginSetCompression(Packet):
    """While not directly related to logging in, this packet is sent by the server during the login process. (Server -> Client)

    :param int comp_thresh: Compression level of future packets, -1 to disable compression.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar comp_thresh:
    """

    id = 0x03
    to = 1

    def __init__(self, comp_thresh: int = -1) -> None:
        super().__init__()

        self.comp_thresh = comp_thresh

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.comp_thresh)
