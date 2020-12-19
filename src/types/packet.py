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
    def pack_msg(cls, msg):
        """Pack a Minecraft chat message into bytes."""

        pass

    def unpack_msg(self):
        """Unpack a Minecraft chat message from bytes."""

        pass
