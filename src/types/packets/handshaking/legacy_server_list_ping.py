from src.types.packet import Packet

__all__ = ('HandshakeLegacyPing',)

class HandshakeLegacyPingToServer(Packet):
    def __init__(self, buf: bytes):
        super.__init__(buf)

        assert self.buf.read(1) == b'\xFE'  # required for legacy slp to be valid

        self.buf.read(15)  # Read constant (unecessary) data

        self.protocol = self.buf.read(1)
        self.hostname = self.read(self.unpack('h'))  # Encoded in UTF-16BE
        self.port = self.unpack('i')
