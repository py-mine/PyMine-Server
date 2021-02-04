import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


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


def test_string():
    buf = Buffer()

    buf.write(Buffer.pack_string(""))
    buf.write(Buffer.pack_string(""))
    buf.write(Buffer.pack_string("2"))
    buf.write(Buffer.pack_string("adkfj;adkfa;ldkfj\x01af\t\n\n00;\xc3\x85\xc3\x84\xc3\x96"))
    buf.write(Buffer.pack_string(""))
    buf.write(Buffer.pack_string("BrUh"))
    buf.write(Buffer.pack_string(""))

    assert buf.unpack_string() == ""
    assert buf.unpack_string() == ""
    assert buf.unpack_string() == "2"
    assert buf.unpack_string() == "adkfj;adkfa;ldkfj\x01af\t\n\n00;\xc3\x85\xc3\x84\xc3\x96"
    assert buf.unpack_string() == ""
    assert buf.unpack_string() == "BrUh"
    assert buf.unpack_string() == ""


def test_json():
    buf = Buffer()

    with open(os.path.join("tests", "sample_data", "test.json")) as test_file:
        data = json.load(test_file)
        buf.write(Buffer.pack_json(data))

    for key, value in buf.unpack_json().items():
        assert key in data
        assert data[key] == value
