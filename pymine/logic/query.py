from __future__ import annotations

import struct
import socket
import asyncio_dgram


class QueryBuffer:
    """Buffer for the query protocol, contains method for dealing with query protocol types.

    :param bytes buf:  Internal bytes object, used to store the data in the QueryBuffer.
    :ivar type pos: The position in the internal bytes/buffer object.
    :ivar buf:
    """

    def __init__(self, buf: bytes = None) -> None:
        self.buf = b"" if buf is None else buf
        self.pos = 0

    def write(self, data: bytes) -> None:
        """Writes data to the buffer.
        :param data: Data to be written to the buffer.
        :type data: bytes
        :return: None
        """

        self.buf += data

    def read(self, length: int = None) -> bytes:
        """
        Reads n bytes from the buffer, if the length is None
        then all remaining data from the buffer is sent.
        :param length: Length in bytes to be read from the buffer.
        :type length: int
        :return: bytes
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

    def unpack_short(self) -> int:
        return struct.unpack("<h", self.read(2))

    @staticmethod
    def pack_magic() -> bytes:
        return b"\xFE\xFD"  # I blame minecraft not me
        # More straightforward, but slower:
        # struct.pack('>H', 65527)

    def unpack_magic(self):
        assert struct.unpack(">H", self.read(2)) == 65277

    @staticmethod
    def pack_string(string: str) -> bytes:
        return bytes(string, "latin-1") + b"\x00"

    def unpack_string(self) -> str:
        out = b""

        while True:
            b = self.read(1)
            if b == b"\x00":  # null byte, end of string
                break
            out += b

        return out.decode("latin-1")

    @staticmethod
    def pack_int32(num: int) -> bytes:
        return struct.pack(">i", num)

    def unpack_int32(self) -> int:
        return struct.unpack(">i", self.read(struct.calcsize(">i")))

    @staticmethod
    def pack_byte(byte: int) -> bytes:
        return struct.pack(">b", byte)


class QueryServer:
    """A query server that supports the Minecraft query protocol.

    :param object server: The PyMine server instance.
    :attr object conf: The contents of server.yml (The server configuration).
    :attr object logger: The instance of the logger.
    :attr server:
    """

    def __init__(self, server):
        self.conf = server.conf
        self.server = server
        self.logger = server.logger  # Logger() instance created by Server.
        self.queryserver = None

    async def start(self):
        self.queryserver = await asyncio_dgram.bind((self.server.addr, self.server.port))
        self.logger.debug(f"Query server started on port {self.server.port}")

    async def stop(self):
        self.logger.info("Shutting down Query server")
