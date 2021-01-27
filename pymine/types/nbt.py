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

    return TAG_Compound.unpack(buf)


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
        raise NotImplementedError(self.__class__.__name__)

    @classmethod
    def unpack_data(cls, buf: Buffer) -> NotImplemented:
        raise NotImplementedError(cls.__name__)

    def pack(self) -> bytes:
        return self.pack_id() + self.pack_name() + self.pack_data()

    @classmethod
    def unpack(cls, buf: Buffer) -> TAG:
        cls.unpack_id(buf)
        return cls(cls.unpack_name(buf), cls.unpack_data(buf))

    def pretty(self, indent: int = 0) -> str:
        return ("    " * indent) + f'{self.__class__.__name__}("{self.name}"): {self.data}'

    def __str__(self):
        return self.pretty()


class TAG_End(TAG):
    id = 0

    def pretty(self, indent: int = 0) -> str:
        return ("    " * indent) + "TAG_End(): 0"


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
    def unpack_data(buf: Buffer) -> int:
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


class TAG_Byte_Array(TAG, bytearray):
    """Used to represent a TAG_Byte_Array, stores an array of bytes.

    :param str name: The name of the TAG.
    :param bytearray data: Some bytes.
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 7

    def __init__(self, name: str, data: bytearray) -> None:
        TAG.__init__(self, name)
        bytearray.__init__(self, data)

    def pack_data(self) -> bytes:
        return Buffer.pack("i", len(self)) + bytes(self)

    @staticmethod
    def unpack_data(buf: Buffer) -> bytearray:
        return bytearray(buf.read(buf.unpack("i")))

    def pretty(self, indent: int = 0) -> str:
        tab = "    " * indent
        tab_extra = "    " * (indent + 1)
        nl = f", "

        return f'{tab}TAG_Int_Array("{self.name}"): [{nl.join([str(v) for v in self])}]'


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

    def pretty(self, indent: int = 0) -> str:
        return ("    " * indent) + f'{self.__class__.__name__}("{self.name}"): {self.data}'


class TAG_List(TAG, list):
    """Represents a TAG_List, a list of nameless and typeless tagss.

    :param str name: The name of the TAG.
    :param list data: A uniform list of TAGs.
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 9

    def __init__(self, name: str, data: list) -> None:
        TAG.__init__(self, name)
        list.__init__(self, data)

    def pack_data(self) -> bytes:
        return Buffer.pack("b", self[0].id) + Buffer.pack("i", len(self)) + b"".join([t.pack_data() for t in self])

    @staticmethod
    def unpack_data(buf: Buffer) -> list:
        tag = TYPES[buf.unpack("b")]
        length = buf.unpack("i")

        out = []

        for _ in range(length):
            out.append(tag(None, tag.unpack_data(buf)))

        return out

    def pretty(self, indent: int = 0) -> str:
        tab = "    " * indent
        nl = f",\n"

        return f'{tab}TAG_List("{self.name}"): [\n{nl.join([t.pretty(indent+1) for t in self])}\n{tab}]'


class TAG_Compound(TAG, dict):
    """Represents a TAG_Compound, a list of named tags.

    :param str name: The name of the TAG.
    :param list data: A list of tags.
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 10

    def __init__(self, name: str, data: list) -> None:
        TAG.__init__(self, name)
        dict.__init__(self, [(t.name, t) for t in data])

    def pack_data(self) -> bytes:
        return b"".join([tag.pack() for tag in self.values()]) + b"\x00"

    @staticmethod
    def unpack_data(buf: Buffer) -> list:
        out = []

        while True:
            tag = TYPES[buf.unpack("b")]

            if tag == TAG_End:
                break

            out.append(tag(tag.unpack_name(buf), tag.unpack_data(buf)))

        return out

    def pretty(self, indent: int = 0) -> str:
        tab = "    " * indent
        nl = f",\n"

        return f'{tab}TAG_Compound("{self.name}"): [\n{nl.join([t.pretty(indent + 1) for t in self.values()])}\n{tab}]'


class TAG_Int_Array(TAG, list):
    """Represents a TAG_Int_Array, a list of ints (4 bytes each).

    :param str name: The name of the TAG.
    :param list data: A list of ints (4 bytes each).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 11

    def __init__(self, name: str, data: list) -> None:
        TAG.__init__(self, name)
        list.__init__(self, data)

    def pack_data(self) -> bytes:
        return Buffer.pack("i", len(self)) + b"".join([Buffer.pack("i", num) for num in self])

    @staticmethod
    def unpack_data(buf: Buffer) -> list:
        return [buf.unpack("i") for _ in range(buf.unpack("i"))]

    def pretty(self, indent: int = 0) -> str:
        tab = "    " * indent
        tab_extra = "    " * (indent + 1)
        nl = f", "

        return f'{tab}TAG_Int_Array("{self.name}"): [{nl.join([str(v) for v in self])}]'


class TAG_Long_Array(TAG, list):
    """Represents a TAG_Long_Array, a list of long longs (8 byte ints).

    :param str name: The name of the TAG.
    :param list value: A list of long longs (8 byte ints).
    :int id: The type ID of the TAG.
    :attr value:
    """

    id = 12

    def __init__(self, name: str, data: list) -> None:
        TAG.__init__(self, name)
        list.__init__(self, data)

    def pack_data(self) -> bytes:
        return Buffer.pack("i", len(self)) + b"".join([Buffer.pack("q", num) for num in self])

    @staticmethod
    def unpack_data(buf: Buffer) -> list:
        return [buf.unpack("q") for _ in range(buf.unpack("i"))]

    def pretty(self, indent: int = 0) -> str:
        tab = "    " * indent
        tab_extra = "    " * (indent + 1)
        nl = f", "

        return f'{tab}TAG_Int_Array("{self.name}"): [{nl.join([str(v) for v in self])}]'


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
