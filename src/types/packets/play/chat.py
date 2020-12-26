"""Contains packets related to the chat."""

from __future__ import annotations
import uuid

from src.types.packet import Packet
from src.types.buffer import Buffer
from src.types.chat import Chat

__all__ = ('PlayChatMessage',)


class PlayChatMessage(Packet):
    """"TODO: make good docstring. (Server -> Client)"""
    id_ = 0x0E

    def __init__(self, data: Chat, position: int, sender: uuid.UUID) -> None:
        super().__init__()
        self.data = data
        self.position = position
        self.sender = sender

    def encode(self):
        return Buffer.pack_chat(self.data) + Buffer.pack('b', self.position) + \
            Buffer.pack_uuid(self.sender)


class PlayTabComplete(Packet):
    """"TODO: make good docstring. (Server -> Client)"""
    id_ = 0x11

    def __init__(self, id: int, start: int, length: int, count: int, matches: list) -> None:
        super().__init__()
        self.id = id
        self.start = start
        self.length = length
        self.count = count
        self.matches = matches

    def encode(self):
        return Buffer.pack_varint(self.id) + Buffer.pack_varint(self.start) + \
            Buffer.pack_varint(self.length) + Buffer.pack_varint(self.count) + \
            Buffer.pack_array(self.matches)


class PlayCloseWindow(Packet):
    """This packet is sent from the server to the client when a window is forcibly closed, such as when a chest is destroyed while it's open. """
    id = 0x12
