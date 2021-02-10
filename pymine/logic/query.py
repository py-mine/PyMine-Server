from __future__ import annotations
import struct

from pymine.server import server


class QueryBuffer:
    """Buffer for the query protocol, will contain most relevant methods."""

    def __init__(self, buf: bytes = None) -> None:
        self.buf = b"" if buf is None else buf
        self.pos = 0

    def write(self, data: bytes) -> None:
        """Writes data to the buffer."""

        self.buf += data

    def read(self, length: int = None) -> bytes:
        """
        Reads n bytes from the buffer, if the length is None
        then all remaining data from the buffer is sent.
        """

        try:
            if length is None:
                length = len(self.buf)
                return self.buf[self.pos :]

            return self.buf[self.pos : self.pos + length]
        finally:
            self.pos += length

    def reset(self) -> None:
        """Resets the position in the buffer."""

        self.pos = 0

    @staticmethod
    def pack_short(short: int) -> bytes:
        return struct.pack("<h", short)

    @staticmethod
    def unpack_short(short: int) -> int:
        return struct.unpack("<h", short)

    @staticmethod
    def pack_magic() -> bytes:
        return b"\xFE\xFD"

    @staticmethod
    def unpack_magic() -> int:
        return 65277  # I hate myself.

    @staticmethod
    def pack_string(string: str) -> bytes:
        return bytes(string, "latin-1") + b"\x00"

    @staticmethod
    def pack_int32(num: int) -> bytes:
        return struct.pack(">i", num)

    @staticmethod
    def unpack_int32(num: int) -> int:  # I think
        return struct.unpack(">i", num)

    @staticmethod
    def pack_byte(byte: int) -> bytes:
        return struct.pack(">b", byte)
