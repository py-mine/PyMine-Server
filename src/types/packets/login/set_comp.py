from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet


class LoginSetCompression(Packet):
    id_ = 0x03

    def __init__(self, comp_thresh: int = -1) -> None:
        super().__init__()

        self.comp_thresh = comp_thresh

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.comp_thresh)
