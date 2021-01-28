import pymine.types.nbt as nbt


class LevelData:  # https://minecraft.gamepedia.com/Java_Edition_level_format#level.dat_format
    def __init__(self, tag: nbt.TAG) -> None:
        tag = tag.get("Data")  # compound

        self.allow_commands = bool(tag.get("allowCommands"))  # default: 0 (byte)

        self.border_center_x = tag.get("BorderCenterX")  # default: 0 (double)
        self.border_center_z = tag.get("BorderCenterZ")  # default: 0 (double)
        self.border_damage_per_block = tag.get("BorderDamagePerBlock")  # default: 0.2 (double)
        self.border_size = tag.get("BorderSize")  # default: 60000000 (double)
        self.border_safe_zone = tag.get("BorderSafeZone")  # default: 5 (double)
        self.border_size_lerp_target = tag.get("BorderSizeLerpTarget")  # default: 60000000 (double)
        self.border_size_lerp_time = tag.get("BorderSizeLerpTime")  # default: 0 (long)
        self.border_warning_blocks = tag.get("BorderWarningBlocks")  # default: 5 (double)
        self.border_warning_time = tag.get("BorderWarningTime")  # default: 15 (double)

        self.clear_weather_time = tag.get("clearWeatherTime")  # default: 0 (int)

        self.custom_boss_events = tag.get("CustomBossEvents")  # compound

        self.datapacks = tag.get("DataPacks")  # compound

        self.data_version = tag.get("DataVersion")  # int

        self.day_time = tag.get("DayTime")  # long

        self.difficulty = tag.get("Difficulty")  # byte
        self.difficulty_locked = tag.get("DifficultyLocked")  # byte

        self.dimension_data = tag.get("DimensionData")  # compound

        self.gamerules = tag.get("GameRules")  # compound

        self.world_gen_settings = tag.get("WorldGenSettings")  # compound

        self.game_type = tag.get("GameType")  # int

        self.generator_name = tag.get("generatorName")  # string
        self.generator_options = tag.get("generatorOptions")  # compound
        self.generator_version = tag.get("generatorVersion")  # int

        self.hardcore = tag.get("hardcore")  # byte

        self.initialized = tag.get("initialized")  # byte

        self.last_played = tag.get("LastPlayed")  # long

        self.level_name = tag.get("LevelName")  # string

        self.map_features = tag.get("MapFeatures")  # byte

        self.player = tag.get("Player")  # compound, probably not used

        self.raining = tag.get("raining")  # byte

        self.rain_time = tag.get("rainTime")  # int

        self.random_seed = tag.get("RandomSeed")  # long

        self.size_on_disk = tag.get("SizeOnDisk")  # long

        self.spawn_x = tag.get("SpawnX")  # int
        self.spawn_y = tag.get("SpawnY")  # int
        self.spawn_z = tag.get("SpawnZ")  # int

        self.thundering = tag.get("thundering")  # byte
        self.thunder_time = tag.get("thunderTime")  # int

        self.time = tag.get("Time")  # long

        self.version = tag.get("version")  # int, the "nbt version of the level"
        self.version_data = tag.get("Version")  # compound

        self.wandering_trader_id = tag.get("WanderingTraderId")  # int array
        self.wandering_trader_spawn_chance = tag.get("WanderingTraderSpawnChance")  # int
        self.wandering_trader_spawn_delay = tag.get("WanderingTraderSpawnDelay")  # int
