import pymine.types.nbt as nbt


class Player:
    def __init__(self, tag: nbt.TAG) -> None:
        self.data_version = tag['DataVersion']  # int

        self.player_game_type = tag['playerGameType']  # int
        self.prev_player_game_type = tag['previousPlayerGameType']  # int

        self.score = tag['Score']  # int

        self.dimension = tag['Dimension']  # str

        self.selected_item_slot = tag['SelectedItemSlot']  # int
        self.selected_item = tag['SelectedItem']  # compound

        self.spawn_dimension = tag['SpawnDimension']  # str
        self.spawn_x = tag['SpawnX']  # int
        self.spawn_y = tag['SpawnY']  # int
        self.spawn_forced = tag['SpawnForced']  # byte

        self.sleep_timer = tag['SleepTimer']  # short

        self.food_level = tag['foodLevel']  # int
        self.food_exhaustion_level = tag['foodExhaustionLevel']  # float
        self.food_saturation_level = tag['foodSaturationLevel']  # float
        self.food_tick_timer = tag['foodTickTimer']  # int

        self.xp_level = tag['XpLevel']  # int
        self.xp_percent = tag['XpP']  # float
        self.xp_total = tag['XpTotal']  # int
        self.xp_seed = tag['XpSeed']  # int

        self.inventory = tag['Inventory']  # list of compound tags
        self.ender_chest = tag['EnderItems']  # list of compound tags

        self.abilities = tag['abilities']  # compound

        self.entered_nether_position = tag['enteredNetherPosition']  # compound

        self.root_vehicle = tag['RootVehicle']  # compound

        self.shoulder_entity_left = tag['ShoulderEntityLeft']  # compound
        self.shoulder_entity_right = tag['ShoulderEntityRight']  # compound

        self.seen_credits = tag['seenCredits']  # byte

        self.recipe_book = tag['recipeBook']  # compound
