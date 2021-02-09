import copy
import os

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt

with open(os.path.join("pymine", "data", "default_nbt", "dimension_codec.nbt"), "rb") as dim_codec_file:
    DEFAULT_DIM_CODEC_NBT = nbt.unpack(Buffer(dim_codec_file.read()), root_is_full=False)


def new_dim_codec_nbt() -> nbt.TAG_Compound:
    return copy.deepcopy(DEFAULT_DIM_CODEC_NBT)


def get_dimension_data(dimension: str) -> nbt.TAG_Compound:
    dims = DEFAULT_DIM_CODEC_NBT["minecraft:dimension_type"]["value"]

    for dim in dims:
        if dim["name"].data.endswith(dimension):  # just in case namespace (like minecraft:) isn't there
            return dim["element"]


# def new_dim_codec_dim_props(
#     piglin_safe: int,
#     natural: int,
#     ambient_light: float,
#     infiniburn: str,
#     respawn_anchor_works: int,
#     has_skylight: int,
#     bed_works: int,
#     effects: str,
#     has_raids: int,
#     logical_height: int,
#     coordinate_scale: float,
#     ultrawarm: int,
#     has_ceiling: int,
#     *,
#     fixed_time: int = None,
# ) -> nbt.TAG_List:
#     out = [
#         nbt.TAG_Byte("piglin_safe", piglin_safe),
#         nbt.TAG_Byte("natural", natural),
#         nbt.TAG_Float("ambient_light", ambient_light),
#         nbt.TAG_String("infiniburn", infiniburn),
#         nbt.TAG_Byte("respawn_anchor_works", respawn_anchor_works),
#         nbt.TAG_Byte("has_skylight", has_skylight),
#         nbt.TAG_Byte("bed_works", bed_works),
#         nbt.TAG_String("effects", effects),
#         nbt.TAG_Byte("has_raids", has_raids),
#         nbt.TAG_Int("logical_height", logical_height),
#         nbt.TAG_Float("coordinate_scale", coordinate_scale),
#         nbt.TAG_Byte("ultrawarm", ultrawarm),
#         nbt.TAG_Byte("has_ceiling", has_ceiling),
#     ]
#
#     if fixed_time:
#         out.append(nbt.TAG_Long("fixed_time", fixed_time))
#
#     return out
#
#
# def new_dim_codec_nbt() -> nbt.TAG_Compound:
#     return nbt.TAG_Compound(
#         "",
#         [
#             nbt.TAG_Compound(
#                 "minecraft:dimension_type",
#                 [  # dimension type registry
#                     nbt.TAG_String("type", "minecraft:dimension_type"),
#                     nbt.TAG_List(
#                         "value",
#                         [  # list of compounds
#                             nbt.TAG_Compound(
#                                 None,
#                                 [
#                                     nbt.TAG_String("name", "minecraft:overworld"),
#                                     nbt.TAG_Int("id", 0),
#                                     nbt.TAG_Compound(
#                                         "element",
#                                         new_dim_codec_dim_props(
#                                             0,
#                                             1,
#                                             0,
#                                             "minecraft:infiniburn_overworld",
#                                             0,
#                                             1,
#                                             1,
#                                             "minecraft:overworld",
#                                             1,
#                                             256,
#                                             1,
#                                             0,
#                                             0,
#                                         ),
#                                     ),
#                                 ],
#                             ),
#                             nbt.TAG_Compound(
#                                 None,
#                                 [
#                                     nbt.TAG_String("name", "minecraft:overworld_caves"),
#                                     nbt.TAG_Int("id", 1),
#                                     nbt.TAG_Compound(
#                                         "element",
#                                         new_dim_codec_dim_props(
#                                             0,
#                                             1,
#                                             0,
#                                             "minecraft:infiniburn_overworld",
#                                             0,
#                                             1,
#                                             1,
#                                             "minecraft:overworld",
#                                             1,
#                                             256,
#                                             1,
#                                             0,
#                                             1,
#                                         ),
#                                     ),
#                                 ],
#                             ),
#                             nbt.TAG_Compound(
#                                 None,
#                                 [
#                                     nbt.TAG_String("name", "minecraft:the_nether"),
#                                     nbt.TAG_Int("id", 2),
#                                     nbt.TAG_Compound(
#                                         "element",
#                                         new_dim_codec_dim_props(
#                                             1,
#                                             0,
#                                             0.1,
#                                             "minecraft:infiniburn_nether",
#                                             1,
#                                             0,
#                                             0,
#                                             "minecraft:the_nether",
#                                             0,
#                                             128,
#                                             8,
#                                             1,
#                                             1,
#                                             fixed_time=18000,
#                                         ),
#                                     ),
#                                 ],
#                             ),
#                             nbt.TAG_Compound(
#                                 None,
#                                 [
#                                     nbt.TAG_String("name", "minecraft:the_end"),
#                                     nbt.TAG_Int("id", 3),
#                                     nbt.TAG_Compound(
#                                         "element",
#                                         new_dim_codec_dim_props(
#                                             0,
#                                             0,
#                                             0,
#                                             "minecraft:infiniburn_end",
#                                             0,
#                                             0,
#                                             0,
#                                             "minecraft:the_end",
#                                             1,
#                                             256,
#                                             1,
#                                             0,
#                                             0,
#                                             fixed_time=6000,
#                                         ),
#                                     ),
#                                 ],
#                             ),
#                         ],
#                     ),
#                 ],
#             ),
#             nbt.TAG_Compound("minecraft:worldgen/biome", []),  # biome registry
#         ],
#     )
