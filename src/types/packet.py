from buffer import Buffer

class Packet(Buffer):
    """Base packet class."""

    def __init__(self, compression_threshold: int = -1):
        Buffer.__init__(self)

        self.id = -0x1
        self.compression_threshold = compression_threshold

    @classmethod
    def from_bytes(cls, data: bytes, comp_thresh: int = -1):
        out = Buffer.from_bytes(data, comp_thresh)

        self.id = self.unpack_varint()
        self.compression_threshold = comp_thresh
