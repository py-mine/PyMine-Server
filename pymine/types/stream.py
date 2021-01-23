from cryptography.hazmat.primitives.ciphers import Cipher
from asyncio import StreamReader, StreamWriter


class Stream(StreamWriter):
    """Used for reading and writing from/to a connected client, merges a StreamReader and StreamWriter."""

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        super().__init__(writer._transport, writer._protocol, writer._reader, writer._loop)

        self.remote = self.get_extra_info("peername")

    def read(self, n: int = -1) -> bytes:
        return self._reader.read(n)

    def readline(self) -> bytes:
        return self._reader.readline()

    def readexactly(self, n: int) -> bytes:
        return self._reader.readexactly(n)

    def readuntil(self, separator: bytes = b"\n") -> bytes:
        return self._reader.readuntil(separator)


class EncryptedStream(Stream):
    def __init__(self, stream: Stream, cipher: Cipher):
        super().__init__(stream._reader, stream)

        self.decryptor = cipher.decryptor()
        self.encryptor = cipher.encryptor()

    async def read(self, n: int = -1):
        return self.decryptor.update(await super().read(n))

    async def readline(self):
        return self.decryptor.update(await super().readline())

    async def readexactly(self, n: int):
        return self.decryptor.update(await super().readexactly(n))

    async def readuntil(self, separator=b"\n"):
        return self.decryptor.update(await super().readuntil(separator))

    def write(self, data: bytes):
        return super().write(self.encryptor.update(data))

    def writelines(self, data: bytes):
        return super().writelines(self.encryptor.update(data))
