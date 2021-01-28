from __future__ import annotations

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

    @classmethod
    def find_chunk_loc(cls, x: int, z: int) -> tuple:
        return cls.find_location_entry(((x % 32) + (z % 32) * 32) * 4)

    @classmethod
    def get_chunk(cls, x: int, z: int) -> NotImplemented:
        raise NotImplementedError

    @classmethod
    def unpack(cls, buf: Buffer) -> Region:
        location_table = [cls.find_location_entry(buf.unpack("i")) for _ in range(1024)]
        timestamp_table = [buf.unpack("i") for _ in range(1024)]
        chunks = [cls.get_chunk()]
