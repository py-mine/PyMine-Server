import struct


class TAG:
    id: int = -1

    def __init__(self) -> None:
        self.id: int = self.__class__.id

    @staticmethod
    def unpack(f: str, buf) -> object:
        unpacked = struct.unpack(">" + f, buf.read(struct.calcsize(f)))

        if len(unpacked) == 1:
            return unpacked[0]

        return unpacked

    @staticmethod
    def pack(f: str, *data: object) -> bytes:
        return struct.pack(">" + f, *data)


class TAG_End(TAG):
    pass


class TAG_Byte(TAG):
    id = 1

    def __init__(self, value: int) -> None:
        super().__init__()

        self.value = value

    def encode(self) -> bytes:
        return struct.pack('')
