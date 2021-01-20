from asyncio import StreamReader, StreamWriter


class Stream(StreamReader, StreamWriter):
    """Used for reading and writing from/to a connected client"""

    def __init__(self, reader: StreamReader, writer: StreamWriter) -> None:
        self.__dict__.extend(reader.__dict__)
        self.__dict__.extend(writer.__dict__)
