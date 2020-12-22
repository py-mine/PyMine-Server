from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet

__all__ = ('HandshakeHandshake',)


class HandshakeHandshake(Packet):  # Serverbound only (client -> server)
    def __init__(self, protocol: int, address: str, port: int, next_state: int, comp_thresh: int = -1) -> None:
        super().__init__(0x00, comp_thresh)

        self.protocol = protocol
        self.address = address
        self.port = port
        self.next_state = next_state

    @classmethod
    def decode(cls, buf: Buffer) -> HandshakeHandshake:
        return cls(buf.unpack_varint(), buf.unpack_string(), buf.unpack('H'), buf.unpack_varint())
