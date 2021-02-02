import pymine.types.nbt as nbt


def new_dim_codec_value_elem(piglin_safe: int, natural: int, ambient_light: float, infiniburn: str, respawn_anchor_works: int, has_skylight: int, bed_works: int, effects: str, has_raids: int, logical_height: int, coordinate_scale: float, ultrawarm: int, has_ceiling: int) -> nbt.TAG_List:
    return [
        nbt.TAG_Byte('piglin_safe', piglin_safe),
        nbt.TAG_Byte('natural', natural),
        nbt.TAG_Float('ambient_light', ambient_light),
        nbt.TAG_String('infiniburn', infiniburn),
        nbt.TAG_Byte('respawn_anchor_works', respawn_anchor_works),
        nbt.TAG_Byte('has_skylight', has_skylight),
        nbt.TAG_Byte('bed_works', bed_works),
        nbt.TAG_String('effects', effects),
        nbt.TAG_Byte('has_raids',  has_raids),
        nbt.TAG_Int('logical_height', logical_height),
        nbt.TAG_Float('coordinate_scale', coordinate_scale),
        nbt.TAG_Byte('ultrawarm', ultrawarm),
        nbt.TAG_Byte('has_ceiling', has_ceiling)
    ]


def new_dim_codec_nbt() -> nbt.TAG_Compound:
    return nbt.TAG_Compound('', [
        nbt.TAG_Compound('minecraft:dimension_type', [  # dimension type registry
            nbt.TAG_String('type', 'minecraft:dimension_type'),
            nbt.TAG_List('value', [  # list of compounds
                nbt.TAG_Compound(None, [
                    nbt.TAG_String('name', 'minecraft:overworld'),
                    nbt.TAG_Int('id', 0),
                    nbt.TAG_Compound('element', new_dim_codec_value_elem(
                        0, 1, 0, "minecraft:infiniburn_overworld", 0, 1, 1, "minecraft:overworld", 1, 256, 1, 0, 0
                    ))
                ]),
                nbt.TAG_Compound(None, [
                    nbt.TAG_String('name', 'minecraft:overworld_caves'),
                    nbt.TAG_Int('id', 0),
                    nbt.TAG_Compound('element', new_dim_codec_value_elem(
                        0, 1, 0, "minecraft:infiniburn_overworld", 0, 1, 1, "minecraft:overworld", 1, 256, 1, 0, 1
                    ))
                ])
            ])
        ]),
        nbt.TAG_Compound('minecraft:worldgen/biome', [  # biome registry

        ])
    ])
