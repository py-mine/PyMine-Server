from __future__ import annotations


class Packet:
    """Base packet class."""

    # id is the packet id (Like 0x00), buf is the bytes/data of the packet,
    # comp_thresh is compression threshold (-1 for no compression)
    def __init__(self, id: int = -0x1, comp_thresh: int = -1) -> None:
        self.id = id
        self.comp_thresh = comp_thresh

    @classmethod
    def decode(cls, data: bytes, comp_thresh: int = -1) -> Packet:
        raise NotImplementedError

    def encode(self) -> bytes:
        raise NotImplementedError
