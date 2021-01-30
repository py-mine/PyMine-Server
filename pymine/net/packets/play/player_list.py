from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chat import Chat

__all__ = ("PlayPlayerListHeaderAndFooter",)


class PlayPlayerListHeaderAndFooter(Packet):
    """yep"""

    id = 0x53
    to = 1

    def __init__(self, header: Chat, footer: Chat) -> None:
        super().__init__()

        self.header = header
        self.footer = footer

    def encode(self) -> bytes:
        return Buffer.pack_chat(self.header) + Buffer.pack_chat(self.footer)
