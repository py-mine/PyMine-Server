from __future__ import annotations

from src.types.buffer import Buffer


class Packet(Buffer):
    """Base packet class."""

    # id is the packet id (Like 0x00), buf is the bytes/data of the packet,
    # direction is either 'toclient', 'toserver', comp_thresh is compression threshold (-1 for no compression)
    def __init__(self, id: int, direction: str, buf: bytes = None, comp_thresh: int = -1) -> None:
        super().__init__(buf)

        self.id = -0x1
        self.direction = direction
        self.comp_thresh = comp_thresh

    @classmethod
    def from_bytes(cls, data: bytes, comp_thresh: int = -1) -> Packet:
        buf = super().from_bytes(data, comp_thresh)

        return cls(buf.unpack_varint(), buf.read(), comp_thresh)

    def to_bytes(self) -> bytes:
        self.buf = self.pack_varint(self.id) + self.buf
        return super().to_bytes(self.comp_thresh)
