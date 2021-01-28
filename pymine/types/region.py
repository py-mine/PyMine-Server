from __future__ import annotations
import zlib

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class Region:
    def __init__(self, location_table: list, timestamp_table: list, chunks: list) -> None:
        self.location_table = location_table
        self.timestamp_table = timestamp_table
        self.chunks = chunks

    @staticmethod  # finds the location of the chunk in the file
    def find_location_entry(loc: int) -> tuple:
        offset = (loc >> 8) & 0xFFFFFF
        size = loc & 0xFF

        return offset * 4096, size * 4096

    # @classmethod
    # def find_chunk_loc(cls, x: int, z: int) -> tuple:
    #     return cls.find_location_entry(((x % 32) + (z % 32) * 32) * 4)

    @classmethod
    def unpack(cls, buf: Buffer) -> Region:
        location_table = [buf.unpack("i") for _ in range(1024)]
        timestamp_table = [buf.unpack("i") for _ in range(1024)]

        chunk_map = {}

        for index, entry in enumerate(location_table):
            loc = cls.find_location_entry(entry)

            chunk_len = buf.unpack('i')
            comp_type = buf.unpack('b')
            chunk = buf.read(chunk_len)

            if comp_type == 0:
                chunk_map[loc[0], loc[1]] = Chunk(loc[0], loc[1], nbt.TAG_Compound.unpack(Buffer(chunk)), timestamp_table[index])
            elif comp_type == 1:
                raise NotImplementedError
            elif comp_type == 2:
                chunk_map[loc[0], loc[1]] = Chunk(
                    loc[0],
                    loc[1],
                    nbt.TAG_Compound.unpack(Buffer(zlib.decompress(chunk))),
                    timestamp_table[index]
                )
            else:
                raise ValueError(f'Value {comp_type} isn\'t a supported compression type.')
