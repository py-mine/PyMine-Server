from __future__ import annotations

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

    @classmethod
    def from_nbt(cls, tag: nbt.TAG) -> Player:
        return cls(
            data_version=tag.get("DataVersion"),  # int
            player_game_type=tag.get("playerGameType"),  # int
            prev_player_game_type=tag.get("previousPlayerGameType"),  # int
            score=tag.get("Score"),  # int
            dimension=tag.get("Dimension"),  # str
            selected_item_slot=tag.get("SelectedItemSlot"),  # int
            selected_item=tag.get("SelectedItem"),  # compound
            spawn_dimension=tag.get("SpawnDimension"),  # str
            spawn_x=tag.get("SpawnX"),  # int
            spawn_y=tag.get("SpawnY"),  # int
            spawn_forced=tag.get("SpawnForced"),  # byte
            sleep_timer=tag.get("SleepTimer"),  # short
            food_level=tag.get("foodLevel"),  # int
            food_exhaustion_level=tag.get("foodExhaustionLevel"),  # float
            food_saturation_level=tag.get("foodSaturationLevel"),  # float
            food_tick_timer=tag.get("foodTickTimer"),  # int
            xp_level=tag.get("XpLevel"),  # int
            xp_percent=tag.get("XpP"),  # float
            xp_total=tag.get("XpTotal"),  # int
            xp_seed=tag.get("XpSeed"),  # int
            inventory=tag.get("Inventory"),  # list of compound tags
            ender_chest=tag.get("EnderItems"),  # list of compound tags
            abilities=tag.get("abilities"),  # compound
            entered_nether_position=tag.get("enteredNetherPosition"),  # compound
            root_vehicle=tag.get("RootVehicle"),  # compound
            shoulder_entity_left=tag.get("ShoulderEntityLeft"),  # compound
            shoulder_entity_right=tag.get("ShoulderEntityRight"),  # compound
            seen_credits=tag.get("seenCredits"),  # byte
            recipe_book=tag.get("recipeBook"),  # compound
        )
