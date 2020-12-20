from __future__ import annotations
import struct

from src.types.message import Message
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

        def to_twos_complement(num, bits):
            return num + (1 << bits) if num < 0 else num

        return struct.pack('>Q', sum((
            to_twos_complement(x, 26) << 38,
            to_twos_complement(y, 12) << 26,
            to_twos_complement(z, 26)
        )))

    def unpack_pos(self) -> tuple:
        """Unpacks a Minecraft position (x, y, z) from the buffer."""

        def from_twos_complement(num, bits):
            if num & (1 << (bits - 1)) != 0:
                num -= (1 << bits)

            return num

        data = self.unpack('>Q')

        x = from_twos_complement(data >> 38, 26)
        y = from_twos_complement(data >> 26 & 0xFFF, 12)
        z = from_twos_complement(data & 0x3FFFFFF, 26)

        return x, y, z
