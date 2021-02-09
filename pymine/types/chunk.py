from __future__ import annotations

import numpy

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class Chunk(nbt.TAG_Compound):
    def __init__(self, tag: nbt.TAG_Compound, timestamp: int) -> None:
        super().__init__("Level", tag["Level"].data)

        self.data_version = tag["DataVersion"]

        self.chunk_x = self["xPos"].data
        self.chunk_z = self["zPos"].data

        self.timestamp = timestamp

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
