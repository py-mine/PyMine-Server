import functools
import os

from pymine.types.buffer import Buffer
from pymine.types.region import Region
from pymine.types.chunk import Chunk


def block_to_chunk_coords(block_x: int, block_z: int) -> tuple:
    return block_x // 16, block_z // 16


def chunk_to_block_coords(chunk_x: int, chunk_z: int) -> tuple:
    return chunk_x * 16, chunk_z * 16


def chunk_to_region_coords(chunk_x: int, chunk_z: int) -> tuple:
    return chunk_x // 32, chunk_z // 32


def region_file_name(chunk_x: int, chunk_z: int) -> str:
    return ".".join(["r", *chunk_to_region_coords(chunk_x, chunk_z), "mca"])


class WorldIO:
    def __init__(self, server):
        self.server = server
    
    async def fetch_region(self, region_file: str, chunk_x: int, chunk_z: int) -> Region:
        if not os.path.isdir(region_file):
            raise NotImplementedError("Region file doesn't exist (and worldgen hasn't been done yet...)")

        return await Region.from_file(region_file)

    def fetch_chunk(self, chunk_x: int, chunk_z: int) -> Chunk:
        raise NotImplementedError
