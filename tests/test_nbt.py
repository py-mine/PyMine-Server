import gzip
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


def test_bigtest():  # tests that loading bigtest.nbt works without errors
    with open(os.path.join("tests", "sample_data", "bigtest.nbt"), "rb") as nbt_file:
        buf = Buffer(nbt_file.read())

    tag = nbt.unpack(buf)

    assert tag.pack() == buf.buf


def test_values_nantest():  # tests that the values for loading the nantest are accurate
    with open(os.path.join("tests", "sample_data", "nantest.nbt"), "rb") as nbt_file:
        tag = nbt.unpack(Buffer(nbt_file.read()))

        assert tag["Air"].data == 300
        assert tag["AttackTime"].data == 0
        assert tag["DeathTime"].data == 0
        assert tag["FallDistance"].data == 0.0
        assert tag["Fire"].data == -20
        assert tag["Health"].data == 20
        assert tag["HurtTime"].data == 0
        assert len(tag["Inventory"]) == 0
        assert len(tag["Motion"]) == 3
        assert tag["Motion"][0].data == 0
        assert tag["Motion"][1].data == 0
        assert tag["Motion"][2].data == 0
        assert tag["OnGround"].data == 1
        assert len(tag["Pos"]) == 3
        assert tag["Pos"][0].data == 0.0
        assert math.isnan(tag["Pos"][1].data)
        assert tag["Pos"][2].data == 0.0
        assert len(tag["Rotation"]) == 2
        assert tag["Rotation"][0].data == 164.3999481201172
        assert tag["Rotation"][1].data == -63.150203704833984
