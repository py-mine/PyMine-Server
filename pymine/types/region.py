from __future__ import annotations
import concurrent.futures
import aiofile
import asyncio
import zlib
import os

from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
import pymine.types.nbt as nbt


# finds the location of the chunk in the file
def find_chunk_pos_in_buffer(loc: int) -> tuple:
    offset = (loc >> 8) & 0xFFFFFF
    # size = loc & 0xFF

    return offset * 4096  # , size * 4096


def region_coords_from_file(file: str) -> tuple:
    return os.path.split(file)[1].split(".")[1:3]


def unpack_chunk_map(buf: Buffer) -> dict:
    location_table = [buf.unpack("i") for _ in range(1024)]
    timestamp_table = [buf.unpack("i") for _ in range(1024)]

    def unpack_chunk(location, timestamp) -> tuple:
        buf.pos = find_chunk_pos_in_buffer(location)

        chunk_len = buf.unpack("i")
        buf.read(1)  # comp type, should always be 2 so ignore

        chunk = Chunk(nbt.TAG_Compound.unpack(Buffer(zlib.decompress(buf.read(chunk_len)))), timestamp)
        # we use mod here to convert to chunk coords INSIDE the region
        return (chunk.chunk_x % 32, chunk.chunk_z % 32), chunk

    return dict(map(unpack_chunk, location_table, timestamp_table))


class Region(dict):
    def __init__(self, chunk_map: dict, region_x: int, region_z: int) -> None:
        dict.__init__(self, chunk_map)

        self.region_x = region_x
        self.region_z = region_z

    @classmethod
    async def from_file(cls, file: str) -> Region:
        async with aiofile.async_open(file, "rb") as region_file:
            buf = Buffer(await region_file.read())

        region_x, region_z = region_coords_from_file(file)

        chunk_map = await asyncio.get_event_loop().run_in_executor(
            concurrent.futures.ProcessPoolExecutor(),
            unpack_chunk_map, buf
        )

        return Region(chunk_map, region_x, region_z)
