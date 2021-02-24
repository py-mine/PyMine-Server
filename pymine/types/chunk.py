from __future__ import annotations

import numpy

from pymine.api.abc import AbstractPalette
from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class ChunkSection:
    """Represents a 16x16x16 area of chunks"""

    def __init__(self, section_y: int, palette: AbstractPalette):
        self.section_y = section_y
        self.palette = palette

        self.block_light = numpy.ndarray((16, 16, 16), numpy.uint8)
        self.states = numpy.ndarray((16, 16, 16), numpy.uint16)
        self.sky_light = numpy.ndarray((16, 16, 16), numpy.uint8)

    def from_nbt(self, tag: nbt.TAG) -> ChunkSection:
        data = Buffer(
            b"".join([Buffer.pack("i", n) for n in tag["BlockLight"]])
            + b"".join([Buffer.pack("i", n) for n in tag["BlockStates"]])
            + b"".join([Buffer.pack("i", n) for n in tag["SkyLight"]])
        )

        bits_per_block = data.read_byte()

        if bits_per_block <= 8:
            palette = IndirectPalette.from_nbt(tag["Palette"])
        else:
            palette = DirectPalette()

        data_array = None

        for y in range(16):
            for z in range(16):
                for x in range(16):
                    block_num = (((y * 16) + z) * 16) + x
                    start_long = (block_num * bits_per_block) / 64
                    start_offset = (block_num * bits_per_block) % 64
                    end_long = ((block_num + 1) * bits_per_block - 1) / 64



class Chunk(nbt.TAG_Compound):
    def __init__(self, tag: nbt.TAG_Compound, sections: numpy.ndarray, timestamp: int) -> None:
        super().__init__("Level", tag["Level"].data)

        self.data_version = tag["DataVersion"]

        self.chunk_x = self["xPos"].data
        self.chunk_z = self["zPos"].data

        self.timestamp = timestamp

        # should be a shape of (256, 16, 16, 3)
        # 16 chunk sections in 256 blocks
        # a chunk section is a 16x16x16 area of blocks
        # each "block" contains (type_id_of_block, block_light_value, sky_light_value)
        # note, this is ***not*** what should be dumped to the disk
        self["Sections"] = sections

    @property
    def sections(self):
        return self["Sections"]

    @classmethod
    def new(cls, chunk_x: int, chunk_z: int, sections: numpy.ndarray, timestamp: int) -> Chunk:
        return cls(cls.new_nbt(chunk_x, chunk_z), sections, timestamp)

    @staticmethod
    def new_nbt(chunk_x: int, chunk_z: int) -> nbt.TAG_Compound:
        return nbt.TAG_Compound(
            "",
            [
                nbt.TAG_Int("DataVersion", 2586),
                nbt.TAG_Compound(
                    "Level",
                    [
                        nbt.TAG_Int_Array("Biomes", []),
                        nbt.TAG_Compound("CarvingMasks", [nbt.TAG_Byte_Array("AIR", []), nbt.TAG_Byte_Array("LIQUID", [])]),
                        nbt.TAG_List("Entities", []),
                        nbt.TAG_Compound(
                            "Heightmaps",
                            [
                                nbt.TAG_Long_Array("MOTION_BLOCKING", []),
                                nbt.TAG_Long_Array("MOTION_BLOCKING_NO_LEAVES", []),
                                nbt.TAG_Long_Array("OCEAN_FLOOR", []),
                                nbt.TAG_Long_Array("OCEAN_FLOOR_WG", []),
                                nbt.TAG_Long_Array("WORLD_SURFACE", []),
                                nbt.TAG_Long_Array("WORLD_SURFACE_WG", []),
                            ],
                        ),
                        nbt.TAG_Long("LastUpdate", 0),
                        nbt.TAG_List("Lights", [nbt.TAG_List(None, []) for _ in range(16)]),
                        nbt.TAG_List("LiquidsToBeTicked", [nbt.TAG_List(None, []) for _ in range(16)]),
                        nbt.TAG_List("LiquidTicks", []),
                        nbt.TAG_Long("InhabitedTime", 0),
                        nbt.TAG_List("PostProcessing", [nbt.TAG_List(None, []) for _ in range(16)]),
                        nbt.TAG_List("Sections", []),
                        nbt.TAG_String("Status", "empty"),
                        nbt.TAG_List("TileEntities", []),
                        nbt.TAG_List("TileTicks", []),
                        nbt.TAG_List("ToBeTicked", [nbt.TAG_List(None, []) for _ in range(16)]),
                        nbt.TAG_Compound("Structures", [nbt.TAG_Compound("References", []), nbt.TAG_Compound("Starts", [])]),
                        nbt.TAG_Int("xPos", chunk_x),
                        nbt.TAG_Int("zPos", chunk_z),
                    ],
                ),
            ],
        )
