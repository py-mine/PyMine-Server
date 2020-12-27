"""Contains statistic packet."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayStatistics',)


class PlayStatistics(Packet):
    """Send data in the stats menu to client. (Server -> Client)

    :param list stats: A list of stat entries (see here: https://wiki.vg/Protocol#Statistics).
    :attr int id_: Unique packet ID.
    :attr stats:
    """

    id_ = 0x06
    to = 1

    def __init__(self, stats: list) -> None:
        super().__init__()

        self.stats = stats

        # Stats should be a list like:
        # [
        #     [category_id: int, statistic_id: int, value: int],
        #     ...
        # ]

    def encode(self) -> bytes:
        out = Buffer.pack_varint(len(self.stats))

        for entry in self.stats:
            out += b''.join(Buffer.pack_varint(e) for e in entry)

        return out
