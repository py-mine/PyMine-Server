# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import numpy
import time

from pymine.types.chunk import Chunk, ChunkSection

from pymine.types.block_palette import DirectPalette
from pymine.types.abc import AbstractWorldGenerator
from pymine.data.registries import BLOCK_REGISTRY

from pymine.server import server


@server.api.register.add_world_generator("superflat")
@server.api.register.add_world_generator("default")
class SuperFlatWorldGenerator(AbstractWorldGenerator):
    @staticmethod
    def generate_chunk(seed: int, dimension: str, chunk_x: int, chunk_z: int) -> Chunk:
        chunk = Chunk.new(chunk_x, chunk_z, int(time.time()))

        chunk.sections[0] = ChunkSection.new(0, DirectPalette)
        palette = chunk.sections[0].palette

        if dimension == "minecraft:overworld":
            chunk.sections[0].block_states[0] = palette.encode("minecraft:bedrock")
            chunk.sections[0].block_states[1:3] = palette.encode("minecraft:dirt")
            chunk.sections[0].block_states[3] = palette.encode("minecraft:grass_block", {"snowy": "false"})

            chunk.sections[0].block_light[0:4] = 0

            chunk.sections[0].sky_light[0:3] = 0
            chunk.sections[0].sky_light[3:] = 15
        elif dimension == "minecraft:nether":
            chunk.sections[0].block_states[0] = palette.encode("minecraft:bedrock")
            chunk.sections[0].block_states[1:4] = palette.encode("minecraft:netherrack")

            chunk.sections[0].block_light[0:4] = 0
            chunk.sections[0].sky_light[4:] = 7
        elif dimension == "minecraft:the_end":
            chunk.sections[0].block_states[0:4] = palette.encode("minecraft:end_stone")

            chunk.sections[0].block_light[0:4] = 0
            chunk.sections[0].sky_light[4:] = 0
        else:
            raise ValueError(f"Unsupported dimension: {dimension}")

        return chunk


# chunk_data = numpy.ndarray((256, 16, 16, 3), numpy.uint16)
#
# if dimension == "minecraft:overworld":
#     chunk_data[0] = (DirectPalette.encode("minecraft:bedrock"), 0, 0)
#     chunk_data[1:3] = (DirectPalette.encode("minecraft:dirt"), 0, 0)
#     chunk_data[4] = (DirectPalette.encode("minecraft:grass_block", {"snowy": "false"}), 0, 15)
# elif dimension == "minecraft:nether":
#     chunk_data[0] = (DirectPalette.encode("minecraft:bedrock"), 0, 0)
#     chunk_data[1:4] = (DirectPalette.encode("minecraft:netherrack"), 0, 6)  # idk what nether sky light level is
# elif dimension == "minecraft:the_end":
#     chunk_data[0:4] = (DirectPalette.encode("minecraft:end_stone"), 0, 6)  # idk what the end sky light level is
# else:
#     raise ValueError(f"Unsupported dimension: {dimension}")
