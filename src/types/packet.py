from __future__ import annotations

from src.data.packet_map import PACKET_MAP

__all__ = ('Packet',)


class Packet:
    """Base Packet class.

    :param int id: Packet identifaction number. Defaults to -0x1.
    :attr id:
    """

    id_ = None

    def __init__(self) -> None:
        self.id_ = self.__class__.id_

    @classmethod
    def from_buf(cls, buf: 'Buffer') -> Packet:
        return PACKET_MAP[state][buf.unpack_varint()].decode(buf)
