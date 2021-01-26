from __future__ import annotations

from pymine.types.buffer import Buffer


class TAG:
    """Base class for an NBT tag.

    :param str name: Name of the tag.
    :attr int id: The type ID.
    :attr name
    """

    id = None

    def __init__(self, name: str = None) -> None:
        self.id = self.__class__.id
        self.name = name


class TAG_End(TAG):
    """Used to represent a TAG_End, signifies the end of a TAG_Compound."""

    id = 0

    def __init__(self) -> None:
        super().__init__()

    def encode(self) -> bytes:
        return b"\x00"

    @classmethod
    def from_buf(cls, buf) -> TAG_End:
        assert buf.unpack("b") == b"\x00"
        return cls()


class TAG_Byte(TAG):
    """Used to represent a TAG_Byte, stores a single signed byte.

    :param int value: A signed byte.
    :attr value:
    """

    id = 1

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("b", self.value)

    @classmethod
    def from_buf(cls, buf) -> TAG_Byte:
        return cls(buf.unpack("b"))


class TAG_Short(TAG):
    """Used to represent a TAG_Short, stores a single short (2 byte int).

    :param int value: A short (number).
    :attr value:
    """

    id = 2

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("h", self.value)

    @classmethod
    def from_buf(cls, buf) -> TAG_Short:
        return cls(buf.unpack("h"))


class TAG_Int(TAG):
    """Used to represent a TAG_Int, stores a single integer (4 bytes).

    :param int value: An integer.
    :attr value:
    """

    id = 3

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("i", self.value)

    @classmethod
    def from_buf(cls, buf) -> TAG_Int:
        return cls(buf.unpack("i"))


class TAG_Long(TAG):
    """Used to represent a TAG_Long, stores a long long (8 byte integer).

    :param int value: A long long (number).
    :attr value:
    """

    id = 4

    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("q", self.value)

    @classmethod
    def from_buf(cls, buf) -> TAG_Long:
        return cls(buf.unpack("q"))


class TAG_Float(TAG):
    """Used to represent a TAG_Float, stores a float (4 bytes).

    :param float value: A float (number).
    :attr value:
    """

    id = 5

    def __init__(self, name: str, value: float) -> None:
        super().__init__(name)

        self.value = value

    def from_buf(self) -> bytes:
        return Buffer.pack("f", self.value)

    @classmethod
    def from_buf(cls, buf) -> TAG_Float:
        return cls(buf.unpack("f"))


class TAG_Double(TAG):
    """Used to represent a TAG_Double, stores a double (8 byte float).

    :param float value: A double (number).
    :attr value:
    """

    id = 6

    def __init__(self, name: str, value: float) -> None:
        super().__init__(name)

        self.value = value

    def encode(self) -> bytes:
        return Buffer.pack("d", self.value)

    @classmethod
    def from_buf(cls, buf) -> TAG_Double:
        return cls(buf.unpack("d"))


class TAG_Byte_Array(TAG):
    """Used to represent a TAG_Byte_Array, stores an array of bytes.

    :param bytes value: Some bytes.
    :attr value:
    """

    id = 7

    def __init__(self, name: str, value: bytes) -> None:
        super().__init__(name)

        self.value = bytearray(value)

    def encode(self) -> bytes:
        return Buffer.pack("i", len(self.value)) + Buffer.pack_array("b", self.value)

    @classmethod
    def from_buf(cls, buf) -> TAG_Byte_Array:
        return cls(buf.unpack_array("b", buf.unpack("i")))


class TAG_String(TAG):
    """Used to represent a TAG_String, stores a string.

    :param str value: A string
    :attr value:
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def encode(self) -> bytes:
        utf8 = self.value.encode("utf8")
        return Buffer.pack("h", len(utf8)) + utf8

    @classmethod
    def from_buf(cls, buf) -> TAG_String:
        return cls(buf.read(buf.unpack("h")).decode("utf8"))


class TAG_List(TAG):
    def __init__(self, value: list) -> None:
        self.value = value

    def encode(self) -> bytes:
        out = b"".join()
