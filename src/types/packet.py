from __future__ import annotations
import struct
import json
import zlib

from src.types.buffer import Buffer


class Packet(Buffer):
    """
    The base class for a packet, contains most
    necessary functions for dealing with the data
    in a packet that isn't covered by a Buffer.
    """

    @classmethod
    def pack_msg(cls, msg) -> bytes:
        """Packs a Minecraft chat message into bytes."""

        pass

    def unpack_msg(self) -> object:
        """Unpacks a Minecraft chat message from the buffer."""

        pass

    @classmethod
    def pack_pos(cls, x, y, z) -> bytes:
        """Packs a Minecraft position (x, y, z) into bytes."""

        pass

    def unpack_pos(self) -> tuple:
        """Unpacks a Minecraft position (x, y, z) from the buffer."""

        pass
