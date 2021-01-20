from asyncio import StreamReader, StreamWriter
from __future__ import annotations


class Stream(StreamReader, StreamWriter):
    """Used for reading and writing from/to a connected client, merges a StreamReader and StreamWriter."""

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        self.original_reader = reader
        self.original_writer = writer

        self.__dict__.extend(reader.__dict__)
        self.__dict__.extend(writer.__dict__)

        self.remote = self.get_extra_info('peername')
