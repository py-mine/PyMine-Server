from asyncio import StreamReader, StreamWriter


class Stream(StreamWriter):
    """Used for reading and writing from/to a connected client, merges a StreamReader and StreamWriter."""

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        StreamWriter.__init__(self, writer._transport, writer._protocol, writer._reader, writer._loop)

        self.reader = self._reader

        self.remote = self.get_extra_info('peername')

    async def read(self, n: int = -1) -> bytes:
        return await self.reader.read(n)

    async def readline(self) -> bytes:
        return await self.reader.readline()

    async def readexactly(self, n: int) -> bytes:
        return await self.reader.readexactly(n)

    async def readuntil(self, separator=b'\n') -> bytes:
        return await self.reader.readuntil(separator)
