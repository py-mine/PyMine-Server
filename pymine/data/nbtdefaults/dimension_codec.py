import pymine.types.nbt as nbt


def new_dim_codec_nbt() -> nbt.TAG_Compound:
    return nbt.TAG_Compound('', [
        nbt.TAG_Compound('minecraft:dimension_type', [  # dimension type registry
            nbt.TAG_String('type', 'minecraft:dimension_type'),
            nbt.TAG_List('value': [  # list of compounds
                nbt.TAG_Compound(None, [
                    nbt.TAG_String('name', 'minecraft:overworld'),
                    nbt.TAG_Int('id', 0),
                    nbt.TAG_Compound('element', [
                        nbt.TAG_Byte()
                    ])
                ])
            ])
        ]),
        nbt.TAG_Compound('minecraft:worldgen/biome', [  # biome registry

        ])
    ])
