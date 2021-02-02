import random
import time

import pymine.types.nbt as nbt


# version (data_version, mc_version, nbt_version)
def new_level_nbt(version: tuple, level_name: str, spawn: tuple, seed: int):
    return nbt.TAG_Compound(
        "",
        nbt.TAG_Compound(
            "Data",
            [
                nbt.TAG_Byte("allowCommands", 0),
                nbt.TAG_Double("BorderCenterX", 0),
                nbt.TAG_Double("BorderCenterZ", 0),
                nbt.TAG_Double("BorderDamagePerBlock", 0.2),
                nbt.TAG_Double("BorderSize", 60000000),
                nbt.TAG_Double("BorderSafeZone", 5),
                nbt.TAG_Double("BorderSizeLerpTarget", 60000000),
                nbt.TAG_Long("BorderSizeLerpTime", 0),
                nbt.TAG_Double("BorderWarningBlocks", 5),
                nbt.TAG_Double("BorderWarningTime", 15),
                nbt.TAG_Double("clearWeatherTime", 0),
                nbt.TAG_Compound("CustomBossEvents", []),
                nbt.TAG_Compound("DataPacks", [nbt.TAG_List("Disabled", []), nbt.TAG_List("Enabled", [])]),
                nbt.TAG_Int("DataVersion", version[0]),
                nbt.TAG_Long("DayTime", 0),
                nbt.TAG_Byte("Difficulty", 2),
                nbt.TAG_Byte("DifficultyLocked", 0),
                nbt.TAG_Compound(
                    "DimensionData",
                    [
                        nbt.TAG_Compound(
                            "1",
                            [
                                nbt.TAG_Compound(
                                    "DragonFight",
                                    [
                                        nbt.TAG_Compound(
                                            "ExitPortalLocation",
                                            [
                                                nbt.TAG_Byte("X", 0),
                                                nbt.TAG_Byte("Y", 100),
                                                nbt.TAG_Byte("Z", 0),
                                            ],
                                        ),
                                        nbt.TAG_List("Gateways", [*map(nbt.TAG_Int, range(19))]),
                                        nbt.TAG_Byte("DragonKilled", 0),
                                        nbt.TAG_Long("DragonUUIDLeast", 0),
                                        nbt.TAG_Long("DragonKilledUUIDMost", 0),
                                        nbt.TAG_Byte("PreviouslyKilled", 0),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                nbt.TAG_Compound(
                    "GameRules",
                    [
                        nbt.TAG_String("announceAdvancements", "true"),
                        nbt.TAG_String("commandBlockOutput", "true"),
                        nbt.TAG_String("disableElytraMovementCheck", "false"),
                        nbt.TAG_String("disableRaids", "false"),
                        nbt.TAG_String("doDaylightCycle", "true"),
                        nbt.TAG_String("doEntityDrops", "true"),
                        nbt.TAG_String("doFireTick", "true"),
                        nbt.TAG_String("doInsomnia", "true"),
                        nbt.TAG_String("doImmediateRespawn", "false"),
                        nbt.TAG_String("doLimitedCrafting", "false"),
                        nbt.TAG_String("doMobLoot", "true"),
                        nbt.TAG_String("doMobSpawning", "true"),
                        nbt.TAG_String("doPatrolSpawning", "true"),
                        nbt.TAG_String("doTileDrops", "true"),
                        nbt.TAG_String("doTraderSpawning", "true"),
                        nbt.TAG_String("doWeatherCycle", "true"),
                        nbt.TAG_String("drowningDamage", "true"),
                        nbt.TAG_String("fallDamage", "true"),
                        nbt.TAG_String("fireDamage", "true"),
                        nbt.TAG_String("forgiveDeadPlayers", "true"),
                        nbt.TAG_String("keepInventory", "false"),
                        nbt.TAG_String("logAdminCommands", "true"),
                        nbt.TAG_String("maxCommandChainLength", "65536"),
                        nbt.TAG_String("maxEntityCramming", "24"),
                        nbt.TAG_String("mobGriefing", "true"),
                        nbt.TAG_String("naturalRegeneration", "true"),
                        nbt.TAG_String("randomTickSpeed", "3"),
                        nbt.TAG_String("reducedDebugInfo", "false"),
                        nbt.TAG_String("sendCommandFeedback", "true"),
                        nbt.TAG_String("showDeathMessages", "true"),
                        nbt.TAG_String("spawnRadius", "10"),
                        nbt.TAG_String("spectatorsGenerateChunks", "true"),
                        nbt.TAG_String("universalAnger", "false"),
                    ],
                ),
                nbt.TAG_Compound(
                    "WorldGenSettings",
                    [
                        nbt.TAG_Byte("bonus_chest", 0),
                        nbt.TAG_Long("seed", seed),
                        nbt.TAG_Byte("generate_features", 1),
                        nbt.TAG_Compound("dimensions", []),
                    ],
                ),
                nbt.TAG_Int("GameType", 0),
                nbt.TAG_Byte("hardcore", 0),
                nbt.TAG_Byte("initialized", 0),
                nbt.TAG_Long("LastPlayed", int(time.time() * 1000)),
                nbt.TAG_Long("LevelName", level_name),
                nbt.TAG_Byte("MapFeatures", 1),
                nbt.TAG_Byte("raining", 0),
                nbt.TAG_Int("rainTime", random.randint(1, 3)*24000),
                nbt.TAG_Long("RandomSeed", seed),
                nbt.TAG_Long("SizeOnDisk", 0),
                nbt.TAG_Int("SpawnX", spawn[0]),
                nbt.TAG_Int("SpawnY", spawn[1]),
                nbt.TAG_Int("SpawnZ", spawn[2]),
                nbt.TAG_Byte("thundering", 0),
                nbt.TAG_Int("thunderTime", random.randint(1, 3)*24000),
                nbt.TAG_Long("Time", 0),
                nbt.TAG_Int("version", version[2]),
                nbt.TAG_Compound(
                    "Version", [nbt.TAG_Int("Id", version[0]), nbt.TAG_String("Name", version[1]), nbt.TAG_Byte("Snapshot", 0)]
                ),
                nbt.TAG_Int_Array("WanderingTraderId", [0, 0, 0, 0]),
                nbt.TAG_Int("WanderingTraderSpawnChance", 50),
                nbt.TAG_Int("WanderingTraderSpawnDelay", 10000),
            ],
        ),
    )
