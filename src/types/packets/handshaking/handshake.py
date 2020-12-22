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
    def decode(self, buf: Buffer) -> HandshakeHandshake:
        return HandshakeHandshake(
            protocol=buf.unpack_varint(),
            address=buf.unpack_string(),
            port=buf.unpack('H'),
            next=buf.unpack_varint()
        )
