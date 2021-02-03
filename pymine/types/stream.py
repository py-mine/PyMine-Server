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
    """An encrypted version of a Stream, automatically encrypts and decrypts outgoing and incoming data.

    :param Stream stream: The original, stream-compatible object.
    :param Cipher cipher: The cipher object, used to encrypt + decrypt data.
    :ivar _CipherContext decryptor: Description of parameter `_CipherContext`.
    :ivar _CipherContext encryptor: Description of parameter `_CipherContext`.
    """

    def __init__(self, stream: Stream, cipher: Cipher) -> None:
        super().__init__(stream._reader, stream)

        self.decryptor = cipher.decryptor()
        self.encryptor = cipher.encryptor()

    async def read(self, n: int = -1) -> bytes:
        return self.decryptor.update(await super().read(n))

    async def readline(self) -> bytes:
        return self.decryptor.update(await super().readline())

    async def readexactly(self, n: int) -> bytes:
        return self.decryptor.update(await super().readexactly(n))

    async def readuntil(self, separator: bytes = b"\n") -> bytes:
        return self.decryptor.update(await super().readuntil(separator))

    def write(self, data: bytes) -> None:
        return super().write(self.encryptor.update(data))

    def writelines(self, data: bytes) -> None:
        return super().writelines(self.encryptor.update(data))
