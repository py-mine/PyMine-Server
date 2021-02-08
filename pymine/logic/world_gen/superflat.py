import numpy
import time

from pymine.types.chunk import Chunk

from pymine.data.block_palette import DirectPalette
from pymine.api.abc import AbstractWorldGenerator
from pymine.data.registries import BLOCK_REGISTRY


class SuperFlatWorldGenerator(AbstractWorldGenerator):

    # Blocks *should* be packed something like this:
    # 256*[16*[16*[block_state_id, block_light, sky_light]]]

    @staticmethod
    def generate_chunk(seed: int, dimension: str, chunk_x: int, chunk_z: int) -> object:
        chunk = Chunk.new(chunk_x, chunk_z, int(time.time()))

        # actual blocks in the chunk
        chunk_blocks = numpy.ndarray((256, 16, 16, 3), numpy.uint16)
        chunk_blocks.fill(DirectPalette.encode("minecraft:air"))

        # if dimension == "minecraft:overworld":
        #     chunk_blocks[0].fill(DirectPalette.encode("minecraft:bedrock"))
        #     chunk_blocks[1:3].fill(DirectPalette.encode("minecraft:dirt"))
        #     chunk_blocks[4].fill(DirectPalette.encode("minecraft:grass_block", {"snowy": "false"}))
        # elif dimension == "minecraft:nether":
        #     chunk_blocks[0].fill(DirectPalette.encode("minecraft:bedrock"))
        #     chunk_blocks[1:4].fill(DirectPalette.encode("minecraft:netherrack"))
        # elif dimension == "minecraft:the_end":
        #     chunk_blocks[0].fill(DirectPalette.encode("minecraft:bedrock"))
        #     chunk_blocks[1:4].fill(DirectPalette.encode("minecraft:end_stone"))

        return chunk_blocks
