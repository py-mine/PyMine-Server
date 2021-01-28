import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymine.types.buffer import Buffer


def test_io():
    buf = Buffer()

    assert buf.buf == b""
    assert buf.pos == 0

    buf = Buffer(b"\x69\x00\x01\x02\x03")

    assert buf.read(1) == b"\x69"
    assert buf.read(2) == b"\x00\x01"
    assert buf.read() == b"\x02\x03"

    buf.reset()
    assert buf.read() == b"\x69\x00\x01\x02\x03"
    buf.reset()


def test_basic():
    buf = Buffer()

    buf.write(Buffer.pack("i", 123) + Buffer.pack("b", 1) + Buffer.pack("?", True) + Buffer.pack("q", 1234567890456))
    assert buf.buf == b"\x00\x00\x00{\x01\x01\x00\x00\x01\x1fq\xfb\x06\x18"

    assert buf.unpack("i") == 123
    assert buf.unpack("b") == 1
    assert buf.unpack("?") is True
    assert buf.unpack("q") == 1234567890456


def test_varint():
    buf = Buffer()

    buf.write(Buffer.pack_varint(0))
    buf.write(Buffer.pack_varint(1))
    buf.write(Buffer.pack_varint(3749146))

    assert buf.unpack_varint() == 0
    assert buf.unpack_varint() == 1
    assert buf.unpack_varint() == 3749146


def test_optional_varint():
    buf = Buffer()

    buf.write(Buffer.pack_optional_varint(1))
    buf.write(Buffer.pack_optional_varint(2))
    buf.write(Buffer.pack_optional_varint(None))
    buf.write(Buffer.pack_optional_varint(3))

    assert buf.unpack_optional_varint() == 1
    assert buf.unpack_optional_varint() == 2
    assert buf.unpack_optional_varint() is None
    assert buf.unpack_optional_varint() == 3
