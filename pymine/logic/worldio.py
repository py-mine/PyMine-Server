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


def region_file_name(chunk_x: int, chunk_z: int) -> tuple:
    raise NotImplementedError


def fetch_chunk(chunk_x: int, chunk_z: int) -> Chunk:
    raise NotImplementedError


def fetch_region(world: str, chunk_x: int, chunk_z: int) -> Region:
    region_file_name = f'' '.'.join(chunk_to_region_coords(chunk_x, chunk_z))
    with open(os.path.join())
