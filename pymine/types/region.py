from __future__ import annotations
import zlib
import os

from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
import pymine.types.nbt as nbt


class Region(dict):
    def __init__(self, chunk_map: dict, region_x: int, region_z: int) -> None:
        dict.__init__(self, chunk_map)

        self.region_x = region_x
        self.region_z = region_z

    @staticmethod  # finds the location of the chunk in the file
    def find_location_entry(loc: int) -> tuple:
        offset = (loc >> 8) & 0xFFFFFF
        size = loc & 0xFF

        return offset * 4096, size * 4096

    # @classmethod
    # def find_chunk_loc(cls, x: int, z: int) -> tuple:
    #     return cls.find_location_entry(((x % 32) + (z % 32) * 32) * 4)

    @classmethod
    def unpack_chunk_map(cls, buf: Buffer) -> dict:
        location_table = [buf.unpack("i") for _ in range(1024)]
        timestamp_table = [buf.unpack("i") for _ in range(1024)]

        chunk_map = {}

        for entry, timestamp in zip(location_table, timestamp_table):
            loc = cls.find_location_entry(entry)

            chunk_len = buf.unpack("i")
            comp_type = buf.unpack("b")
            chunk = buf.read(chunk_len)

            if comp_type == 0:  # no compression
                chunk_map[loc[0], loc[1]] = Chunk(loc[0], loc[1], nbt.TAG_Compound.unpack(Buffer(chunk)), timestamp)
            elif comp_type == 1:  # gzip, shouldn't ever be used
                raise NotImplementedError
            elif comp_type == 2:  # zlib compression
                chunk_map[loc[0], loc[1]] = Chunk(
                    loc[0], loc[1], nbt.TAG_Compound.unpack(Buffer(zlib.decompress(chunk))), timestamp
                )
            else:
                raise ValueError(f"Value {comp_type} isn't a supported compression type.")

        return chunk_map

    @classmethod
    def from_file(cls, file: str) -> Region:
        with open(file, 'rb') as region_file:
            buf = Buffer(region_file.read())

        region_x, region_z = os.path.split(file)[1].split('.')[1:3]
        chunk_map = cls.unpack_chunk_map(buf)

        return Region(chunk_map, region_x, region_z)
