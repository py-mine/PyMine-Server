from asyncio import StreamReader, StreamWriter


class Stream(StreamWriter):
    """Used for reading and writing from/to a connected client, merges a StreamReader and StreamWriter."""

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        StreamWriter.__init__(self, writer._transport, writer._protocol, writer._reader, writer._loop)

        self.remote = self.get_extra_info('peername')

        self.reader = self._reader

        self.read = self.reader.read
        self.readline = self.reader.readline
        self.readexactly = self.reader.readactly
        self.readuntil = self.reader.readuntil
