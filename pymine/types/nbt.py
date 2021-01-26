from __future__ import annotations

from mutf8 import encode_modified_utf8, decode_modified_utf8
import gzip

from pymine.types.buffer import Buffer

TYPES = []


def from_buf(buf: Buffer) -> TAG_Compound:
    try:
        buf = Buffer(gzip.decompress(buf.read()))
    except BaseException:
        pass

    return TAG_Compound.from_buf(buf)


class TAG:
    """Base class for an NBT tag.

    :param str name: The name of the TAG.
    :attr int id: The type ID.
    :attr name
    """

    id = None

    def __init__(self, name: str = None) -> None:
        self.id = self.__class__.id
        self.name = name

    def pack_id(self) -> bytes:
        return Buffer.pack("b", self.id)

    @staticmethod
    def unpack_id(buf: Buffer) -> int:
        return buf.unpack("b")

    def pack_name(self) -> bytes:
        mutf8_name = encode_modified_utf8(self.name)
        return Buffer.pack("H", len(mutf8_name)) + mutf8_name

    @staticmethod
    def unpack_name(buf: Buffer) -> str:
        return decode_modified_utf8(buf.read(buf.unpack("H")))

    def pack_data(self) -> bytes:
        raise NotImplementedError

    @staticmethod
    def unpack_data(buf: Buffer) -> NotImplemented:
        raise NotImplementedError

    def pack(self) -> bytes:
        return self.pack_id() + self.pack_name() + self.pack_data()

    @classmethod
    def unpack(cls, buf: Buffer) -> TAG:
        cls.unpack_id(buf)
        return cls(cls.unpack_name(buf), cls.unpack_data(buf))

    def pretty(self, obj: object = None, i: int = 0):
        if obj is None:
            obj = self

        t = "  " * i

        if isinstance(obj, TAG):
            return f"{t}{type(obj).__name__}({obj.name})[\n{self.pretty(obj.value, i+1)}\n{t}]"
        elif isinstance(obj, list):
            return f",\n{t}".join([self.pretty(val, i + 1) for val in obj])
        else:
            return f"{t}{obj}"


class TAG_End(TAG):
    id = 0


class TAG_Byte(TAG):
    """Used to represent a TAG_Byte, stores a single signed byte.

    :param str name: The name of the TAG.
    :param int data: A signed byte.
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 1

    def __init__(self, name: str, data: int) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("b", self.data)

    @staticmethod
    def unpack_data(buf: Buffer) -> int:
        return buf.unpack("b")


class TAG_Short(TAG):
    """Used to represent a TAG_Short, stores a single short (2 byte int).

    :param str name: The name of the TAG.
    :param int data: A short (2 byte int).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 2

    def __init__(self, name: str, data: int) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("h", self.data)

    @staticmethod
    def unpack_data(buf: Buffer) -> int:
        return buf.unpack("h")


class TAG_Int(TAG):
    """Used to represent a TAG_Int, stores an integer (4 bytes).

    :param str name: The name of the TAG.
    :param int data: A int (4 bytes).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 3

    def __init__(self, name: str, data: int) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("i", self.data)

    @staticmethod
    def unpack_data(buf: Buffer) -> int:
        return buf.unpack("i")


class TAG_Long(TAG):
    """Used to represent a TAG_Long, stores a long long (8 byte int).

    :param str name: The name of the TAG.
    :param int data: A long long (8 byte int).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 4

    def __init__(self, name: str, data: int) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("q", self.data)

    @staticmethod
    def pack_data(buf: Buffer) -> int:
        return buf.unpack("q")


class TAG_Float(TAG):
    """Used to represent a TAG_Float, stores a float (4 bytes).

    :param str name: The name of the TAG.
    :param float data: A float (4 bytes).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 5

    def __init__(self, name: str, data: float) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("f", self.data)

    @staticmethod
    def unpack_data(buf: Buffer) -> float:
        return buf.unpack("f")


class TAG_Double(TAG):
    """Used to represent a TAG_Double, stores a double (8 byte float).

    :param str name: The name of the TAG.
    :param float data: A double (8 byte float).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 6

    def __init__(self, name: str, data: float) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("d", self.data)

    @staticmethod
    def unpack_data(buf: Buffer) -> float:
        return buf.unpack("d")


class TAG_Byte_Array(TAG):
    """Used to represent a TAG_Byte_Array, stores an array of bytes.

    :param str name: The name of the TAG.
    :param bytearray data: Some bytes.
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 7

    def __init__(self, name: str, data: bytearray) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("i", len(self.data)) + bytes(self.data)

    @staticmethod
    def unpack_data(buf: Buffer) -> bytearray:
        return bytearray(buf.read(buf.unpack("i")))


class TAG_String(TAG):
    """Used to represent a TAG_String, stores a string.

    :param str name: The name of the TAG.
    :param str data: A string.
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 8

    def __init__(self, name: str, data: str) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        mutf8_text = encode_modified_utf8(self.data)
        return Buffer.pack("H", len(mutf8_text)) + mutf8_text

    @staticmethod
    def unpack_data(buf: Buffer) -> str:
        return decode_modified_utf8(buf.read(buf.unpack("H")))


class TAG_List(TAG):
    """Represents a TAG_List, a list of nameless and typeless tagss.

    :param str name: The name of the TAG.
    :param list data: A uniform list of TAGs.
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 9

    def __init__(self, name: str, data: list) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return (
            Buffer.pack("b", self.data[0].id)
            + Buffer.pack("i", len(self.data))
            + b"".join([t.pack_id() + t.pack_data() for t in self.data])
        )

    @staticmethod
    def unpack_data(buf: Buffer) -> list:
        tag = TYPES[buf.unpack("b")]
        length = buf.unpack("i")

        out = []

        for _ in range(length):
            tag.unpack_id(buf)

            out.append(tag(None, tag.unpack_data(buf)))

        return out


class TAG_Compound(TAG):
    """Represents a TAG_Compound, a list of named tags.

    :param str name: The name of the TAG.
    :param list data: A list of tags.
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 10

    def __init__(self, name: str, data: list) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return b"".join([tag.pack() for tag in self.data]) + b"\x00"

    @staticmethod
    def unpack_data(buf: Buffer) -> list:
        out = []

        while True:
            tag = TYPES[buf.read(1)]

            if tag == TAG_End:
                break

            out.append(tag(tag.unpack_name(buf), tag.unpack_data(buf)))

        return out


class TAG_Int_Array(TAG):
    """Represents a TAG_Int_Array, a list of ints (4 bytes each).

    :param str name: The name of the TAG.
    :param list data: A list of ints (4 bytes each).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 11

    def __init__(self, name: str, data: list) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("i", len(self.data)) + b"".join([Buffer.pack("i", num) for num in self.data])

    @staticmethod
    def unpack_data(buf: Buffer) -> list:
        return [buf.unpack("i") for _ in range(buf.unpack("i"))]


class TAG_Long_Array(TAG):
    """Represents a TAG_Long_Array, a list of long longs (8 byte ints).

    :param str name: The name of the TAG.
    :param list value: A list of long longs (8 byte ints).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 12

    def __init__(self, name: str, data: list) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return Buffer.pack("i", len(self.data)) + b"".join([Buffer.pack("q", num) for num in self.data])

    @staticmethod
    def unpack_data(buf: Buffer) -> list:
        return [buf.unpack("q") for _ in range(buf.unpack("i"))]


TYPES.extend(
    [
        TAG_End,
        TAG_Byte,
        TAG_Short,
        TAG_Int,
        TAG_Long,
        TAG_Float,
        TAG_Double,
        TAG_Byte_Array,
        TAG_String,
        TAG_List,
        TAG_Compound,
        TAG_Int_Array,
        TAG_Long_Array,
    ]
)
