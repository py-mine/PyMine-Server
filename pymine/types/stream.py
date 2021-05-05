# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from cryptography.hazmat.primitives.ciphers import Cipher
from asyncio import StreamReader, StreamWriter


class Stream(StreamWriter):
    """Used for reading and writing from/to a connected client, merges a StreamReader and StreamWriter.

    :param StreamReader reader: An asyncio.StreamReader instance.
    :param StreamWriter writer: An asyncio.StreamWriter instance.
    :ivar tuple remote: A tuple which stores the remote client's address and port.
    """

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
