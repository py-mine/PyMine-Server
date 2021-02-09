from __future__ import annotations

import random
import struct
import uuid

import pymine.types.nbt as nbt


class Player:
    def __init__(self, entity_id: int, data: nbt.TAG) -> None:
        self.entity_id = entity_id
        self.data = data

        self.uuid = uuid.UUID(bytes=struct.pack(">iiii", *data["UUID"]))
        self.x, self.y, self.z = self.pos = data["Pos"]

        self.remote = None

        self.username = None
        self.brand = None
        self.locale = None
        self.view_distance = None
        self.chat_mode = None
        self.chat_colors = None
        self.displayed_skin_parts = None
        self.main_hand = None

    @classmethod
    def new(cls, entity_id: int, uuid_: uuid.UUID, spawn: tuple, dimension: str) -> Player:
        return cls(entity_id, cls.new_nbt(uuid_, spawn, dimension))

    @staticmethod
    def new_nbt(uuid_: uuid.UUID, spawn: tuple, dimension: str) -> nbt.TAG:
        return nbt.TAG_Compound(
            "",
            [
                nbt.TAG_List("Pos", [nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0)]),
                nbt.TAG_List("Motion", [nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0)]),
                nbt.TAG_List("Rotation", [nbt.TAG_Float(None, 0), nbt.TAG_Float(None, 0)]),
                nbt.TAG_Float("FallDistance", 0),
                nbt.TAG_Short("Fire", -20),
                nbt.TAG_Short("Air", 300),
                nbt.TAG_Byte("OnGround", 1),
                nbt.TAG_Byte("NoGravity", 0),
                nbt.TAG_Byte("Invulnerable", 0),
                nbt.TAG_Int("PortalCooldown", 0),
                nbt.TAG_Int_Array("UUID", struct.unpack(">iiii", uuid_.bytes)),
                nbt.TAG_String("CustomName", ""),
                nbt.TAG_Byte("CustomNameVisible", 0),
                nbt.TAG_Byte("Silent", 0),
                nbt.TAG_List("Passengers", []),
                nbt.TAG_Byte("Glowing", 0),
                nbt.TAG_List("Tags", []),
                nbt.TAG_Float("Health", 20),
                nbt.TAG_Float("AbsorptionAmount", 0),
                nbt.TAG_Short("HurtTime", 0),
                nbt.TAG_Int("HurtByTimestamp", 0),
                nbt.TAG_Short("DeathTime", 0),
                nbt.TAG_Byte("FallFlying", 0),
                # nbt.TAG_Int('SleepingX', 0),
                # nbt.TAG_Int('SleepingY', 0),
                # nbt.TAG_Int('SleepingZ', 0),
                nbt.TAG_Compound("Brain", [nbt.TAG_Compound("memories", [])]),
                nbt.TAG_List(
                    "ivaributes",
                    [
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.max_health"),
                                nbt.TAG_Double("Base", 20),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.follow_range"),
                                nbt.TAG_Double("Base", 32),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.knockback_resistance"),
                                nbt.TAG_Double("Base", 0),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.movement_speed"),
                                nbt.TAG_Double("Base", 1),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.attack_damage"),
                                nbt.TAG_Double("Base", 2),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.armor"),
                                nbt.TAG_Double("Base", 0),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.armor_toughness"),
                                nbt.TAG_Double("Base", 0),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.attack_knockback"),
                                nbt.TAG_Double("Base", 0),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [
                                nbt.TAG_String("Name", "generic.attack_speed"),
                                nbt.TAG_Double("Base", 4),
                                nbt.TAG_List("Modifiers", []),
                            ],
                        ),
                        nbt.TAG_Compound(
                            None,
                            [nbt.TAG_String("Name", "generic.luck"), nbt.TAG_Double("Base", 0), nbt.TAG_List("Modifiers", [])],
                        ),
                    ],
                ),
                nbt.TAG_List("ActiveEffects", []),
                nbt.TAG_Int("DataVersion", 2586),
                nbt.TAG_Int("playerGameType", 0),
                nbt.TAG_Int("previousPlayerGameType", -1),
                nbt.TAG_Int("Score", 0),
                nbt.TAG_String("Dimension", dimension),
                nbt.TAG_Int("SelectedItemSlot", 0),
                nbt.TAG_Compound(
                    "SelectedItem",
                    [nbt.TAG_Byte("Count", 1), nbt.TAG_String("id", "minecraft:air"), nbt.TAG_Compound("tag", [])],
                ),
                nbt.TAG_String("SpawnDimension", "overworld"),
                nbt.TAG_Int("SpawnX", spawn[0]),
                nbt.TAG_Int("SpawnY", spawn[1]),
                nbt.TAG_Int("SpawnZ", spawn[2]),
                nbt.TAG_Byte("SpawnForced", 0),
                nbt.TAG_Int("foodLevel", 20),
                nbt.TAG_Float("foodExhaustionLevel", 0),
                nbt.TAG_Float("foodSaturationLevel", 5),
                nbt.TAG_Int("foodTickTimer", 0),
                nbt.TAG_Int("XpLevel", 0),
                nbt.TAG_Float("XpP", 0),
                nbt.TAG_Int("XpTotal", 0),
                nbt.TAG_Int("XpSeed", random.randint(-2147483648, 2147483647)),
                nbt.TAG_List("Inventory", []),
                nbt.TAG_List("EnderItems", []),
                nbt.TAG_Compound(
                    "abilities",
                    [
                        nbt.TAG_Float("walkSpeed", 0.1),
                        nbt.TAG_Float("flySpeed", 0.05),
                        nbt.TAG_Byte("mayfly", 0),
                        nbt.TAG_Byte("flying", 0),
                        nbt.TAG_Byte("invulnerable", 0),
                        nbt.TAG_Byte("mayBuild", 1),
                        nbt.TAG_Byte("instabuild", 0),
                    ],
                ),
                # nbt.TAG_Compound('enteredNetherPosition', [nbt.TAG_Double('x', 0), nbt.TAG_Double('y', 0), nbt.TAG_Double('z', 0)]),
                # nbt.TAG_Compound('RootVehicle', [
                #     nbt.TAG_Int_Array('Attach', [0, 0, 0, 0]),
                #     nbt.TAG_Compound('Entity', [])
                # ]),
                nbt.TAG_Byte("seenCredits", 0),
                nbt.TAG_Compound(
                    "recipeBook",
                    [
                        nbt.TAG_List("recipes", []),
                        nbt.TAG_List("toBeDisplayed", []),
                        nbt.TAG_Byte("isFilteringCraftable", 0),
                        nbt.TAG_Byte("isGuiOpen", 0),
                        nbt.TAG_Byte("isFurnaceFilteringCraftable", 0),
                        nbt.TAG_Byte("isFurnaceGuiOpen", 0),
                        nbt.TAG_Byte("isBlastingFurnaceFilteringCraftable", 0),
                        nbt.TAG_Byte("isBlastingFurnaceGuiOpen", 0),
                        nbt.TAG_Byte("isSmokerFilteringCraftable", 0),
                        nbt.TAG_Byte("isSmokerGuiOpen", 0),
                    ],
                ),
            ],
        )

    def __str__(self) -> str:
        return self.username
