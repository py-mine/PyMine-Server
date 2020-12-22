from src.types.packet import Packet

__all__ = ('HandshakeHandshake',)

class HandshakeHandshake(Packet):  # Serverbound (client -> server) only
    def __init__(self, buf: bytes, comp_thresh = -1):
        super().__init__(0x00, buf, comp_thresh)

        self.protocol = super().unpack_varint()
        self.address = super().unpack_string()
        self.port = super().unpack('H')
        self.next_state = super().unpack_varint()
