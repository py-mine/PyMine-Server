"""Contains LoginSetCompression which is technically part of the login process."""

from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet

__all__ = ('LoginSetCompression',)


class LoginSetCompression(Packet):
    """While not directly related to logging in, this packet is sent by the server during the login process.

    Parameters
    ----------
    comp_thresh : int
        Compression threshold to be sent to the server, -1 to disable.

    Attributes
    ----------
    id_ : int
        Unique packet ID
    comp_thresh
    """

    id_ = 0x03

    def __init__(self, comp_thresh: int = -1) -> None:
        super().__init__()

        self.comp_thresh = comp_thresh

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.comp_thresh)
