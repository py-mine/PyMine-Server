import gzip
import os

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


def test_loading_bigtest():  # tests that loading bigtest.nbt works without errors
    with open(os.path.join("tests", "sample_nbt", "bigtest.nbt"), 'rb') as nbt_file:
        tag = nbt.unpack(Buffer(nbt_file.read()))


def test_dumping_bigtest():  # tests that the data dumping/tag packing works properly
    with open(os.path.join("tests", "sample_nbt", "bigtest.nbt"), 'rb') as nbt_file:
        buf_old = Buffer(gzip.decompress(nbt_file.read()))

        tag = nbt.unpack(Buffer(buf_old.buf))
        tag_bytes = tag.pack()

        assert tag_bytes == buf_old.read()


def test_dumping_nantest():  # tests that the data dumping/tag packing works properly for a file that uses NaN
    with open(os.path.join("tests", "sample_nbt", "nantest.nbt"), 'rb') as nbt_file:
        buf_old = Buffer(gzip.decompress(nbt_file.read()))

        tag = nbt.unpack(Buffer(buf_old.buf))
        tag_bytes = tag.pack()

        assert tag_bytes == buf_old.read()
