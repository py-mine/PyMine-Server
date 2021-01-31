import pymine.types.nbt as nbt


class Player:
    def __init__(
        self,
        *,
        data_version: int,
        player_game_type: int,
        prev_player_game_type: int,
        score: int,
        dimension: str,
        selected_item_slot: int,
        selected_item: nbt.TAG_Compound,
        spawn_dimension: str,
        spawn_x: int,
        spawn_y: int,
        spawn_forced: bool,
        sleep_timer: int,
        food_level: int,
        food_exhaustion_level: float,
        food_saturation_level: float,
        food_tick_timer: int,
        xp_level: int,
        xp_percent: float,
        xp_total: int,
        xp_seed: int,
        inventory: nbt.TAG_List,
        ender_chest: nbt.TAG_List,
        abilities: nbt.TAG_Compound,
        entered_nether_position: nbt.TAG_Compound,
        root_vehicle: nbt.TAG_Compound,
        shoulder_entity_left: nbt.TAG_Compound,
        shoulder_entity_right: nbt.TAG_Compound,
        seen_credits: bool,
        recipe_book: nbt.TAG_Compound,
    ) -> None:
        pass

    # def __init__(self, tag: nbt.TAG) -> None:
    #     self.data_version = tag.get("DataVersion")  # int
    #
    #     self.player_game_type = tag.get("playerGameType")  # int
    #     self.prev_player_game_type = tag.get("previousPlayerGameType")  # int
    #
    #     self.score = tag.get("Score")  # int
    #
    #     self.dimension = tag.get("Dimension")  # str
    #
    #     self.selected_item_slot = tag.get("SelectedItemSlot")  # int
    #     self.selected_item = tag.get("SelectedItem")  # compound
    #
    #     self.spawn_dimension = tag.get("SpawnDimension")  # str
    #     self.spawn_x = tag.get("SpawnX")  # int
    #     self.spawn_y = tag.get("SpawnY")  # int
    #     self.spawn_forced = tag.get("SpawnForced")  # byte
    #
    #     self.sleep_timer = tag.get("SleepTimer")  # short
    #
    #     self.food_level = tag.get("foodLevel")  # int
    #     self.food_exhaustion_level = tag.get("foodExhaustionLevel")  # float
    #     self.food_saturation_level = tag.get("foodSaturationLevel")  # float
    #     self.food_tick_timer = tag.get("foodTickTimer")  # int
    #
    #     self.xp_level = tag.get("XpLevel")  # int
    #     self.xp_percent = tag.get("XpP")  # float
    #     self.xp_total = tag.get("XpTotal")  # int
    #     self.xp_seed = tag.get("XpSeed")  # int
    #
    #     self.inventory = tag.get("Inventory")  # list of compound tags
    #     self.ender_chest = tag.get("EnderItems")  # list of compound tags
    #
    #     self.abilities = tag.get("abilities")  # compound
    #
    #     self.entered_nether_position = tag.get("enteredNetherPosition")  # compound
    #
    #     self.root_vehicle = tag.get("RootVehicle")  # compound
    #
    #     self.shoulder_entity_left = tag.get("ShoulderEntityLeft")  # compound
    #     self.shoulder_entity_right = tag.get("ShoulderEntityRight")  # compound
    #
    #     self.seen_credits = tag.get("seenCredits")  # byte
    #
    #     self.recipe_book = tag.get("recipeBook")  # compound
