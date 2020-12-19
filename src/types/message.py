from __future__ import annotations

from src.types.buffer import Buffer


class Message:
    """
    A Minecraft chat message
    """

    def __init__(self, msg):
        self.msg = msg

    @classmethod
    def from_buf(cls, buf: Buffer) -> Message:
        """Creates a Minecraft chat message from a buffer"""

        return cls(buf.unpack_json())

    @classmethod
    def from_string(cls, text: str) -> Message:
        """Creates a Minecraft chat message from json"""

        return cls({'text': text})

    def to_bytes(self) -> bytes:
        """Converts a Minecraft chat message to bytes"""

        return Buffer.pack_json(self.msg)

    def to_string(self):
        """Converts a Minecraft chat message to text"""

        pass
