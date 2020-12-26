"""Contains packets related to the chat."""

from __future__ import annotations
import uuid

from src.types.packet import Packet
from src.types.buffer import Buffer
from src.types.chat import Chat

__all__ = ('PlayChatMessage',)


class PlayChatMessage(Packet):
    """"TODO: make good docstring. (Server -> Client)""
    id_ = 0x0E

    def __init__(self, data: Chat, position: int, sender: uuid.UUID) -> None:
        super().__init__()
        self.data = data
        self.position = position
        self.sender = sender

    def encode(self):
        return Buffer.pack_chat(self.data) + Buffer.pack('b', self.position) + \
        Buffer.pack_uuid(self.sender)
