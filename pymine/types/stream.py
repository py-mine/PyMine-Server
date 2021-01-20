from asyncio import StreamReader, StreamWriter


class Stream(StreamWriter):
    """Used for reading and writing from/to a connected client, merges a StreamReader and StreamWriter."""

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        super().__init__(writer._transport, writer._protocol, writer._reader, writer._loop)

        self.remote = self.get_extra_info('peername')

    async def read(self, n: int = -1) -> bytes:
        return await self._reader.read(n)

    async def readline(self) -> bytes:
        return await self._reader.readline()

    async def readexactly(self, n: int) -> bytes:
        return await self._reader.readexactly(n)

    async def readuntil(self, separator=b'\n') -> bytes:
        return await self._reader.readuntil(separator)
