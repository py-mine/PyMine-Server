from __future__ import annotations

import aiofile

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class LevelData:  # https://minecraft.gamepedia.com/Java_Edition_level_format#level.dat_format
    def __init__(
        self,
        *,
        allow_commands: bool,
        border_center_x: float,
        border_center_z: float,
        border_damage_per_block: float,
        border_size: float,
        border_safe_zone: float,
        border_size_lerp_target: float,
        border_size_lerp_time: int,
        border_warning_blocks: float,
        border_warning_time: float,
        clear_weather_time: int,
        custom_boss_events: nbt.TAG_Compound,
        datapacks: nbt.TAG_Compound,
        data_version: int,
        day_time: int,
        difficulty: int,
        difficulty_locked: bool,
        dimension_data: nbt.TAG_Compound,
        gamerules: nbt.TAG_Compound,
        world_gen_settings: nbt.TAG_Compound,
        game_type: int,
        generator_name: str,
        generator_options: nbt.TAG_Compound,
        generator_version: int,
        hardcore: bool,
        initialized: bool,
        last_played: int,
        level_name: str,
        map_features: bool,
        player: nbt.TAG_Compound,
        raining: bool,
        rain_time: int,
        random_seed: int,
        size_on_disk: int,
        spawn_x: int,
        spawn_y: int,
        spawn_z: int,
        thundering: bool,
        thunder_time: int,
        time: int,
        version: int,
        version_data: nbt.TAG_Compound,
        wandering_trader_id: list,
        wandering_trader_spawn_chance: int,
        wandering_trader_spawn_delay: int,
    ) -> None:
        allow_commands = allow_commands

        self.border_center_x = border_center_x
        self.border_center_z = border_center_z
        self.border_damage_per_block = border_damage_per_block
        self.border_size = border_size
        self.border_safe_zone = border_safe_zone
        self.border_size_lerp_target = border_size_lerp_target
        self.border_size_lerp_time = border_size_lerp_time
        self.border_warning_blocks = border_warning_blocks
        self.border_warning_time = border_warning_time

        self.clear_weather_time = clear_weather_time

        self.custom_boss_events = custom_boss_events

        self.datapacks = datapacks

        self.data_version = data_version

        self.day_time = day_time

        self.difficulty = difficulty
        self.difficulty_locked = difficulty_locked

        self.dimension_data = dimension_data

        self.gamerules = gamerules

        self.world_gen_settings = world_gen_settings

        self.game_type = game_type

        self.generator_name = generator_name
        self.generator_options = generator_options
        self.generator_version = generator_version

        self.hardcore = hardcore

        self.initialized = initialized

        self.last_played = last_played

        self.level_name = level_name

        self.map_features = map_features

        self.player = player

        self.raining = raining
        self.rain_time = rain_time

        self.random_seed = random_seed

        self.size_on_disk = size_on_disk

        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.spawn_z = spawn_z

        self.thundering = thundering
        self.thunder_time = thunder_time

        self.time = time

        self.version = version
        self.version_data = version_data

        self.wandering_trader_id = wandering_trader_id
        self.wandering_trader_spawn_chance = wandering_trader_spawn_chance
        self.wandering_trader_spawn_delay = wandering_trader_spawn_delay

    @classmethod
    async def from_file(cls, file: str) -> LevelData:
        async with aiofile.async_open(file, "rb") as level_data_file:
            return cls.from_nbt(nbt.TAG_Compound.unpack(Buffer(await level_data_file.read())))

    @classmethod
    def from_nbt(cls, tag: nbt.TAG) -> LevelData:
        tag = tag.get("Data")  # compound

        return cls(
            allow_commands=bool(tag.get("allowCommands")),  # default: 0 (byte)
            border_center_x=tag.get("BorderCenterX"),  # default: 0 (double)
            border_center_z=tag.get("BorderCenterZ"),  # default: 0 (double)
            border_damage_per_block=tag.get("BorderDamagePerBlock"),  # default: 0.2 (double)
            border_size=tag.get("BorderSize"),  # default: 60000000 (double)
            border_safe_zone=tag.get("BorderSafeZone"),  # default: 5 (double)
            border_size_lerp_target=tag.get("BorderSizeLerpTarget"),  # default: 60000000 (double)
            border_size_lerp_time=tag.get("BorderSizeLerpTime"),  # default: 0 (long)
            border_warning_blocks=tag.get("BorderWarningBlocks"),  # default: 5 (double)
            border_warning_time=tag.get("BorderWarningTime"),  # default: 15 (double)
            clear_weather_time=tag.get("clearWeatherTime"),  # default: 0 (int)
            custom_boss_events=tag.get("CustomBossEvents"),  # compound
            datapacks=tag.get("DataPacks"),  # compound
            data_version=tag.get("DataVersion"),  # int
            day_time=tag.get("DayTime"),  # long
            difficulty=tag.get("Difficulty"),  # byte
            difficulty_locked=bool(tag.get("DifficultyLocked")),  # byte
            dimension_data=tag.get("DimensionData"),  # compound
            gamerules=tag.get("GameRules"),  # compound
            world_gen_settings=tag.get("WorldGenSettings"),  # compound
            game_type=tag.get("GameType"),  # int
            generator_name=tag.get("generatorName"),  # string
            generator_options=tag.get("generatorOptions"),  # compound
            generator_version=tag.get("generatorVersion"),  # int
            hardcore=bool(tag.get("hardcore")),  # byte
            initialized=bool(tag.get("initialized")),  # byte
            last_played=tag.get("LastPlayed"),  # long
            level_name=tag.get("LevelName"),  # string
            map_features=tag.get("MapFeatures"),  # byte
            player=tag.get("Player"),  # compound, probably not used
            raining=bool(tag.get("raining")),  # byte
            rain_time=tag.get("rainTime"),  # int
            random_seed=tag.get("RandomSeed"),  # long
            size_on_disk=tag.get("SizeOnDisk"),  # long
            spawn_x=tag.get("SpawnX"),  # int
            spawn_y=tag.get("SpawnY"),  # int
            spawn_z=tag.get("SpawnZ"),  # int
            thundering=bool(tag.get("thundering")),  # byte
            thunder_time=tag.get("thunderTime"),  # int
            time=tag.get("Time"),  # long
            version=tag.get("version"),  # int, the "nbt version of the level"
            version_data=tag.get("Version"),  # compound
            wandering_trader_id=tag.get("WanderingTraderId"),  # int array
            wandering_trader_spawn_chance=tag.get("WanderingTraderSpawnChance"),  # int
            wandering_trader_spawn_delay=tag.get("WanderingTraderSpawnDelay"),  # int
        )

    @staticmethod
    def default_nbt():
        return nbt.TAG_Compound('', nbt.TAG_Compound('Data', [
            nbt.TAG_Byte('allowCommands', 0),
            nbt.TAG_Double('BorderCenterX', 0),
            nbt.TAG_Double('BorderCenterZ', 0),
            nbt.TAG_Double('BorderDamagePerBlock', 0.2),
            nbt.TAG_Double('BorderSize', 60000000),
            nbt.TAG_Double('BorderSafeZone', 5),
            nbt.TAG_Double('BorderSizeLerpTarget', 60000000),
            nbt.TAG_Long('BorderSizeLerpTime', 0),
            nbt.TAG_Double('BorderWarningBlocks', 5),
            nbt.TAG_Double('BorderWarningTime', 15),
            nbt.TAG_Double('clearWeatherTime', 0),
            nbt.TAG_Compound('CustomBossEvents', []),
            nbt.TAG_Compound('DataPacks', []),
            nbt.TAG_Int('DataVersion', 2586),
            nbt.TAG_Long('DayTime', 0),
            nbt.TAG_Byte('Difficulty', 2),
            nbt.TAG_Byte('DifficultyLocked', 0),
            nbt.TAG_Compound('DimensionData', [
                nbt.TAG_Compound('1', [
                    nbt.TAG_Compound('DragonFight', [
                        nbt.TAG_Compound('ExitPortalLocation', [
                            nbt.TAG_Byte('X', 0),
                            nbt.TAG_Byte('Y', 100),
                            nbt.TAG_Byte('Z', 0),
                        ]),
                        nbt.TAG_List('Gateways', [nbt.TAG_Int(i) for i in range(19)]),
                        nbt.TAG_Byte('DragonKilled', 0),
                        nbt.TAG_Long('DragonUUIDLeast', 0),
                        nbt.TAG_Long('DragonKilledUUIDMost', 0),
                        nbt.TAG_Byte('PreviouslyKilled', 0)
                    ])
                ])
            ]),
            nbt.TAG_Compound('GameRules', [
                nbt.TAG_String('announceAdvancements', 'true'),
                nbt.TAG_String('commandBlockOutput', 'true'),
                nbt.TAG_String('disableElytraMovementCheck', 'false'),
                nbt.TAG_String('disableRaids', 'false'),
                nbt.TAG_String('doDaylightCycle', 'true'),
                nbt.TAG_String('doEntityDrops', 'true'),
                nbt.TAG_String('doFireTick', 'true'),
                nbt.TAG_String('doInsomnia', 'true'),
                nbt.TAG_String('doImmediateRespawn', 'false')
            ])
        ]))
