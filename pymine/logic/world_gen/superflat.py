import ctypes
import numpy

from pymine.types.chunk import Chunk

from pymine.data.registries import BLOCK_REGISTRY
from pymine.api.world_gen import AbstractWorldGenerator


class SuperFlatWorldGenerator(AbstractWorldGenerator):
    def generate_chunk(self, chunk_x: int, chunk_z: int) -> Chunk:

        # actual blocks in the chunk
        chunk_blocks = numpy.ndarray((256, 16, 16), numpy.uint16)
        chunk_blocks.fill(BLOCK_REGISTRY.encode('minecraft:air'))
        chunk_blocks[0].fill(BLOCK_REGISTRY.encode('minecraft:bedrock'))
        chunk_blocks[1:3].fill(BLOCK_REGISTRY.encode('minecraft:dirt'))
        chunk_blocks[4].fill(BLOCK_REGISTRY.encode('minecraft:grass_block'))

        
