"""Contains packets related to the chat."""

from __future__ import annotations
import uuid

from src.types.packet import Packet
from src.types.buffer import Buffer
from src.types.chat import Chat

__all__ = (
    'PlayChatMessageClientBound',
    'PlayTabComplete',
)


class PlayChatMessageClientBound(Packet):
    """A chat message from the server to the client (Server -> Client)

    :param Chat data: The actual chat data.
    :param int position: Where on the GUI the message is to be displayed.
    :param uuid.UUID sender: Unknown, see here: https://wiki.vg/Protocol#Chat_Message_.28clientbound.29.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr data:
    :attr position:
    :attr sender:
    """

    id = 0x0E
    to = 1

    def __init__(self, data: Chat, position: int, sender: uuid.UUID) -> None:
        super().__init__()

        self.data = data
        self.position = position
        self.sender = sender

    def encode(self) -> bytes:
        return Buffer.pack_chat(self.data) + Buffer.pack('b', self.position) + \
            Buffer.pack_uuid(self.sender)


class PlayTabComplete(Packet):
    """"TODO: make good docstring. (Server -> Client)"""

    id = 0x11
    to = 1

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
