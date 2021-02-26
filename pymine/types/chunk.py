from __future__ import annotations

import numpy

from pymine.types.block_palette import DirectPalette, IndirectPalette
from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt

from pymine.api.abc import AbstractPalette


class ChunkSection:
    """Represents a 16x16x16 area of chunks"""

    def __init__(self, y: int, palette: AbstractPalette):
        self.y = y
        self.palette = palette

        self.block_states = None
        self.block_light = None
        self.sky_light = None

    @classmethod
    def from_nbt(cls, tag: nbt.TAG) -> ChunkSection:
        if tag.get("BlockStates") is not None:
            # this is a calculation one would use to serialize a chunk section
            # we need this to solve for bits_per_block as we don't have that
            # but we *do* have the length of the array from the nbt data
            # that we read earlier
            # long_array_len = ((16*16*16)*bits_per_block) / 64
            # this simplifies to 64*bits_per_block which is easy to solve
            # for bits_per_block so we get the below
            bits_per_block = len(tag["BlockStates"]) // 64  # probably 4

            individual_value_mask = (1 << bits_per_block) - 1

            if tag.get("Palette") is None:
                palette = DirectPalette()
            else:
                palette = IndirectPalette.from_nbt(tag["Palette"])

            section = cls(tag["Y"].data, palette)

            section.block_states = numpy.ndarray((16, 16, 16), numpy.uint16)

            # yoinked most of the logic for chunk deserialization from https://wiki.vg/Chunk_Format
            # however, that is for deserialization of a chunk packet, not the nbt data so it's a bit
            # different but most of the logic still applies and this is needed for that
            state_bytes = b"".join([Buffer.pack("q", n) for n in tag["BlockStates"]])

            # populate block_states array
            for y in range(16):
                for z in range(16):
                    for x in range(16):
                        block_num = (((y * 16) + z) * 16) + x
                        start_long = (block_num * bits_per_block) // 64
                        start_offset = (block_num * bits_per_block) % 64
                        end_long = ((block_num + 1) * bits_per_block - 1) // 64

                        if start_long == end_long:
                            data = state_bytes[start_long] >> start_offset
                        else:
                            data = state_bytes[start_long] >> start_offset | state_bytes[end_long] << (64 - start_offset)

                        section.block_states[x, y, z] = data & individual_value_mask
        else:
            section = cls(tag["Y"], None)

        # the light arrays (SkyLight and BlockLight) are byte arrays (8 bits), and four bits are used per block

        if tag.get("BlockLight") is None:
            section.block_light = None
        else:
            section.block_light = numpy.asarray(
                [n for n in ((b & 0x0F, b >> 4 & 0x0F) for b in tag["BlockLight"])], numpy.uint8
            ).reshape(16, 16, 16)

        if tag.get("SkyLight") is None:
            section.sky_light = None
        else:
            section.sky_light = numpy.asarray(
                [n for n in ((b & 0x0F, b >> 4 & 0x0F) for b in tag["SkyLight"])], numpy.uint8
            ).reshape(16, 16, 16)

        return section


class Chunk(dict):
    def __init__(self, tag: nbt.TAG_Compound, timestamp: int) -> None:
        super().__init__(dict(tag["Level"]))

        self.data_version = tag["DataVersion"]

        self.x = self["xPos"].data
        self.z = self["zPos"].data

        self.timestamp = timestamp

        self.sections = {}  # indexes go below 0 so a dict it is

        for section_tag in self["Sections"]:
            self.sections[section_tag["Y"].data] = ChunkSection.from_nbt(section_tag)

        # delete data which are stored as attributes of this class
        del self["Sections"]  # stored in .sections
        del self["xPos"]
        del self["zPos"]

    @classmethod
    def new(cls, chunk_x: int, chunk_z: int, timestamp: int) -> Chunk:
        return cls(cls.new_nbt(chunk_x, chunk_z), timestamp)

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
