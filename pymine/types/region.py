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
    def find_chunk_pos_in_buffer(loc: int) -> tuple:
        offset = (loc >> 8) & 0xFFFFFF
        # size = loc & 0xFF

        return offset * 4096  # , size * 4096

    @staticmethod  # converts chunk coords to be region relative
    def chunk_coords_to_region_relative(chunk_x: int, chunk_z: int) -> tuple:
        return chunk_x % 32, chunk_z % 32

    @classmethod
    def unpack_chunk_map(cls, buf: Buffer) -> dict:
        location_table = [buf.unpack("i") for _ in range(1024)]
        timestamp_table = [buf.unpack("i") for _ in range(1024)]

        def unpack_chunk(entry_timestamp) -> tuple:
            entry, timestamp = entry_timestamp

            buf.pos = cls.find_chunk_pos_in_buffer(entry)

            chunk_len = buf.unpack("i")
            comp_type = buf.unpack("b")
            chunk = buf.read(chunk_len)

            if comp_type == 2:  # zlib
                chunk = Chunk(nbt.TAG_Compound.unpack(Buffer(zlib.decompress(chunk))), timestamp)
                return cls.chunk_coords_to_region_relative(chunk.chunk_x, chunk.chunk_z), chunk

            if comp_type == 0:
                chunk = Chunk(nbt.TAG_Compound.unpack(Buffer(chunk)), timestamp)
                return cls.chunk_coords_to_region_relative(chunk.chunk_x, chunk.chunk_z), chunk

            raise ValueError(f"Value {comp_type} isn't a supported compression type.")

        return dict(map(unpack_chunk, zip(location_table, timestamp_table)))

    @classmethod
    def from_file(cls, file: str) -> Region:
        with open(file, "rb") as region_file:
            buf = Buffer(region_file.read())

        region_x, region_z = os.path.split(file)[1].split(".")[1:3]
        chunk_map = cls.unpack_chunk_map(buf)

        return Region(chunk_map, region_x, region_z)
