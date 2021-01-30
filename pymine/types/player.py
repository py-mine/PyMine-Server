import pymine.types.nbt as nbt


class Player:
    def __init__(self, tag: nbt.TAG) -> None:
        self.data_version = tag.get('DataVersion')  # int

        self.player_game_type = tag.get('playerGameType')  # int
        self.prev_player_game_type = tag.get('previousPlayerGameType')  # int

        self.score = tag.get('Score')  # int

        self.dimension = tag.get('Dimension')  # str

        self.selected_item_slot = tag.get('SelectedItemSlot')  # int
        self.selected_item = tag.get('SelectedItem')  # compound

        self.spawn_dimension = tag.get('SpawnDimension')  # str
        self.spawn_x = tag.get('SpawnX')  # int
        self.spawn_y = tag.get('SpawnY')  # int
        self.spawn_forced = tag.get('SpawnForced')  # byte

        self.sleep_timer = tag.get('SleepTimer')  # short

        self.food_level = tag.get('foodLevel')  # int
        self.food_exhaustion_level = tag.get('foodExhaustionLevel')  # float
        self.food_saturation_level = tag.get('foodSaturationLevel')  # float
        self.food_tick_timer = tag.get('foodTickTimer')  # int

        self.xp_level = tag.get('XpLevel')  # int
        self.xp_percent = tag.get('XpP')  # float
        self.xp_total = tag.get('XpTotal')  # int
        self.xp_seed = tag.get('XpSeed')  # int

        self.inventory = tag.get('Inventory')  # list of compound tags
        self.ender_chest = tag.get('EnderItems')  # list of compound tags

        self.abilities = tag.get('abilities')  # compound

        self.entered_nether_position = tag.get('enteredNetherPosition')  # compound

        self.root_vehicle = tag.get('RootVehicle')  # compound

        self.shoulder_entity_left = tag.get('ShoulderEntityLeft')  # compound
        self.shoulder_entity_right = tag.get('ShoulderEntityRight')  # compound

        self.seen_credits = tag.get('seenCredits')  # byte

        self.recipe_book = tag.get('recipeBook')  # compound
