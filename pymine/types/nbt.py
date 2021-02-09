from __future__ import annotations

from mutf8 import encode_modified_utf8, decode_modified_utf8
import struct
import gzip

__all__ = (
    "TAG",
    "TAG_End",
    "TAG_Byte",
    "TAG_Short",
    "TAG_Int",
    "TAG_Long",
    "TAG_Float",
    "TAG_Double",
    "TAG_Byte_Array",
    "TAG_String",
    "TAG_List",
    "TAG_Compound",
    "TAG_Int_Array",
    "TAG_Long_Array",
    "TYPES",
    "unpack",
)

TYPES = []


def unpack(buf, root_is_full: bool = True) -> TAG_Compound:
    try:
        data = gzip.decompress(buf.buf[buf.pos :])
        buf.buf = data
        buf.reset()
    except BaseException:
        pass

    if root_is_full:
        buf.read(1)
        return TAG_Compound(TAG.unpack_name(buf), TAG_Compound.unpack_data(buf))

    return TAG_Compound(None, TAG_Compound.unpack_data(buf))


class BufferUtil:
    @staticmethod
    def unpack(buf, f: str) -> object:
        unpacked = struct.unpack(">" + f, buf.read(struct.calcsize(f)))

        if len(unpacked) == 1:
            return unpacked[0]

        return unpacked

    @staticmethod
    def pack(f: str, *data: object) -> bytes:
        return struct.pack(">" + f, *data)


class TAG:
    """Base class for an NBT tag.

    :param str name: The name of the TAG.
    :ivar int id: The type ID.
    :ivar name
    """

    id = None

    def __init__(self, name: str = None) -> None:
        self.id = self.__class__.id
        self.name = "" if name is None else name

    def pack_id(self) -> bytes:
        return BufferUtil.pack("b", self.id)

    @staticmethod
    def unpack_id(buf) -> int:
        return buf.unpack("b")

    def pack_name(self) -> bytes:
        mutf8_name = encode_modified_utf8(self.name)
        return BufferUtil.pack("H", len(mutf8_name)) + mutf8_name

    @staticmethod
    def unpack_name(buf) -> str:
        return decode_modified_utf8(buf.read(buf.unpack("H")))

    def pack_data(self) -> bytes:
        raise NotImplementedError(self.__class__.__name__)

    @classmethod
    def unpack_data(cls, buf) -> NotImplemented:
        raise NotImplementedError(cls.__name__)

    def pack(self) -> bytes:
        return self.pack_id() + self.pack_name() + self.pack_data()

    @classmethod
    def unpack(cls, buf) -> TAG:
        cls.unpack_id(buf)
        return cls(cls.unpack_name(buf), cls.unpack_data(buf))

    def pretty(self, indent: int = 0) -> str:
        return ("    " * indent) + f'{self.__class__.__name__}("{self.name}"): {self.data}'

    def __str__(self):
        return self.pretty()


class TAG_End(TAG):
    id = 0

    def __init__(self, *args) -> None:
        super().__init__(None)

    def pack_name(self) -> bytes:
        return b""

    @staticmethod
    def unpack_name(buf) -> None:
        return None

    def pack_data(self) -> bytes:
        return b""

    @staticmethod
    def unpack_data(buf) -> None:
        pass

    def pretty(self, indent: int = 0) -> str:
        return ("    " * indent) + "TAG_End(): 0"


class TAG_Byte(TAG):
    """Used to represent a TAG_Byte, stores a single signed byte.

    :param str name: The name of the TAG.
    :param int data: A signed byte.
    :int id: The type ID of the TAG.
    :ivar value:
    """

    id = 1

    def __init__(self, name: str, data: int) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return BufferUtil.pack("b", self.data)

    @staticmethod
    def unpack_data(buf) -> int:
        return buf.unpack("b")


class TAG_Short(TAG):
    """Used to represent a TAG_Short, stores a single short (2 byte int).

    :param str name: The name of the TAG.
    :param int data: A short (2 byte int).
    :int id: The type ID of the TAG.
    :ivar value:
    """

    id = 2

    def __init__(self, name: str, data: int) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return BufferUtil.pack("h", self.data)

    @staticmethod
    def unpack_data(buf) -> int:
        return buf.unpack("h")


class TAG_Int(TAG):
    """Used to represent a TAG_Int, stores an integer (4 bytes).

    :param str name: The name of the TAG.
    :param int data: A int (4 bytes).
    :int id: The type ID of the TAG.
    :ivar value:
    """

    id = 3

    def __init__(self, name: str, data: int) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return BufferUtil.pack("i", self.data)

    @staticmethod
    def unpack_data(buf) -> int:
        return buf.unpack("i")


class TAG_Long(TAG):
    """Used to represent a TAG_Long, stores a long long (8 byte int).

    :param str name: The name of the TAG.
    :param int data: A long long (8 byte int).
    :int id: The type ID of the TAG.
    :ivar value:
    """

    id = 4

    def __init__(self, name: str, data: int) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return BufferUtil.pack("q", self.data)

    @staticmethod
    def unpack_data(buf) -> int:
        return buf.unpack("q")


class TAG_Float(TAG):
    """Used to represent a TAG_Float, stores a float (4 bytes).

    :param str name: The name of the TAG.
    :param float data: A float (4 bytes).
    :int id: The type ID of the TAG.
    :ivar value:
    """

    id = 5

    def __init__(self, name: str, data: float) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return BufferUtil.pack("f", self.data)

    @staticmethod
    def unpack_data(buf) -> float:
        return buf.unpack("f")


class TAG_Double(TAG):
    """Used to represent a TAG_Double, stores a double (8 byte float).

    :param str name: The name of the TAG.
    :param float data: A double (8 byte float).
    :int id: The type ID of the TAG.
    :ivar value:
    """

    id = 6

    def __init__(self, name: str, data: float) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        return BufferUtil.pack("d", self.data)

    @staticmethod
    def unpack_data(buf) -> float:
        return buf.unpack("d")


class TAG_Byte_Array(TAG, bytearray):
    """Used to represent a TAG_Byte_Array, stores an array of bytes.

    :param str name: The name of the TAG.
    :param bytearray data: Some bytes.
    :int id: The type ID of the TAG.
    :ivar value:
    """

    id = 7

    def __init__(self, name: str, data: bytearray) -> None:
        TAG.__init__(self, name)

        if isinstance(data, str):
            print(f"WARNING: data passed was not bytes ({repr(data)})")
            data = data.encode("utf8")

        bytearray.__init__(self, data)

    def pack_data(self) -> bytes:
        return BufferUtil.pack("i", len(self)) + bytes(self)

    @staticmethod
    def unpack_data(buf) -> bytearray:
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
    :ivar value:
    """

    id = 8

    def __init__(self, name: str, data: str) -> None:
        super().__init__(name)

        self.data = data

    def pack_data(self) -> bytes:
        mutf8_text = encode_modified_utf8(self.data)
        return BufferUtil.pack("H", len(mutf8_text)) + mutf8_text

    @staticmethod
    def unpack_data(buf) -> str:
        return decode_modified_utf8(buf.read(buf.unpack("H")))

    def pretty(self, indent: int = 0) -> str:
        return ("    " * indent) + f'{self.__class__.__name__}("{self.name}"): {self.data}'


class TAG_List(TAG, list):
    """Represents a TAG_List, a list of nameless and typeless tagss.

    :param str name: The name of the TAG.
    :param list data: A uniform list of TAGs.
    :int id: The type ID of the TAG.
    :ivar value:
    """

    id = 9

    def __init__(self, name: str, data: list) -> None:
        TAG.__init__(self, name)
        list.__init__(self, data)

    def pack_data(self) -> bytes:
        if len(self) > 0:
            return BufferUtil.pack("b", self[0].id) + BufferUtil.pack("i", len(self)) + b"".join([t.pack_data() for t in self])
        else:
            return BufferUtil.pack("b", 0) + BufferUtil.pack("i", 0)

    @staticmethod
    def unpack_data(buf) -> list:
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
    :ivar value:
    """

    id = 10

    def __init__(self, name: str, data: list) -> None:
        TAG.__init__(self, name)
        dict.__init__(self, [(t.name, t) for t in data])

    @property
    def data(self):
        return self.values()

    def __setitem__(self, key, value):
        value.name = key
        dict.__setitem__(self, key, value)

    def update(self, *args, **kwargs):
        dict.update(self, *args, **kwargs)

        for k, v in self.items():
            v.name = k

    def pack_data(self) -> bytes:
        return b"".join([tag.pack() for tag in self.values()]) + b"\x00"

    @staticmethod
    def unpack_data(buf) -> list:
        out = []

        while True:
            tag = TYPES[buf.unpack("b")]

            if tag is TAG_End:
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
    :ivar value:
    """

    id = 11

    def __init__(self, name: str, data: list) -> None:
        TAG.__init__(self, name)
        list.__init__(self, data)

    def pack_data(self) -> bytes:
        return BufferUtil.pack("i", len(self)) + b"".join([BufferUtil.pack("i", num) for num in self])

    @staticmethod
    def unpack_data(buf) -> list:
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
    :ivar value:
    """

    id = 12

    def __init__(self, name: str, data: list) -> None:
        TAG.__init__(self, name)
        list.__init__(self, data)

    def pack_data(self) -> bytes:
        return BufferUtil.pack("i", len(self)) + b"".join([BufferUtil.pack("q", num) for num in self])

    @staticmethod
    def unpack_data(buf) -> list:
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
