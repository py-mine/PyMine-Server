"""Contains packets related to advancements."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = (
    'PlayAdvancementTab',
    'PlaySelectAdvancementTab',
)


class PlayAdvancementTab(Packet):
    """Related to advancement tab menu, see here: https://wiki.vg/Protocol#Advancement_Tab (Client -> Server)

    :param int action: Either opened tab (0), or closed screen (1).
    :param int tab_id: The ID of the tab, only present if action is 0 (opened tab)
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr action:
    :attr tab_id:
    """

    id = 0x22
    to = 0

    def __init__(self, action: int, tab_id: int) -> None:
        super().__init__()

        self.action = action
        self.tab_id = tab_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayAdvancementTab:
        return cls(buf.unpack_varint(), (buf.unpack_varint() if buf.unpack('?') else None))


class PlaySelectAdvancementTab(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x3C
    to = 1

    def __init__(self, identifier: str = None) -> None:
        super().__init__()

        self.identifier = identifier

    def encode(self) -> bytes:
        return Buffer.pack_optional(Buffer.pack_string, self.identifier)
