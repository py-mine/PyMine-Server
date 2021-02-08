import numpy
import time

from pymine.types.chunk import Chunk

from pymine.data.block_palette import DirectPalette
from pymine.api.abc import AbstractWorldGenerator
from pymine.data.registries import BLOCK_REGISTRY


class SuperFlatWorldGenerator(AbstractWorldGenerator):

    # Blocks *should* be packed something like this:
    # 256*[16*[16*[block_state_id, block_light, sky_light]]]

    class Break(BaseException):
        pass

    @staticmethod
    def generate_chunk(seed: int, dimension: str, chunk_x: int, chunk_z: int) -> numpy.ndarray:
        chunk = Chunk.new(chunk_x, chunk_z, int(time.time()))

        # actual blocks in the chunk
        chunk_blocks = numpy.ndarray((256, 16, 16, 3), numpy.uint16)
        chunk_blocks.fill(DirectPalette.encode("minecraft:air"))  # should be 0

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

        if dimension == 'minecraft:overworld':
            chunk_blocks[0] = (DirectPalette.encode("minecraft:bedrock"), 0, 0)
            chunk_blocks[1:3] = (DirectPalette.encode("minecraft:dirt"), 0, 0)
            chunk_blocks[4] = (DirectPalette.encode("minecraft:grass_block", {"snowy": "false"}), 0, 15)
        elif dimension == 'minecraft:nether':
            chunk_blocks[0] = (DirectPalette.encode("minecraft:bedrock"), 0, 0)
            chunk_blocks[1:4] = (DirectPalette.encode("minecraft:netherrack"), 0, 6)  # idk what nether sky light level is
        elif dimension == "minecraft:the_end":
            chunk_blocks[0:4] = (DirectPalette.encode("minecraft:end_stone"), 0, 6)  # idk what the end sky light level is
        else:
            raise ValueError(f"Unsupported dimension: {dimension}")

        return chunk_blocks
