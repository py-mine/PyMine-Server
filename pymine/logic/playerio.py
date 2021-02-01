import aiofile
import uuid
import os

from pymine.types.buffer import Buffer
from pymine.types.player import Player
import pymine.types.nbt as nbt


class PlayerDataIO:
    def __init__(self, level_name: str):
        self.level_name = level_name
        self.data_dir = os.path.join("worlds", level_name, "playerdata")
        self.cache = {}

    async def fetch_player(self, uuid_: uuid.UUID) -> Player:
        try:
            return self.cache[int(uuid_)]
        except KeyError:
            file = os.path.join(self.data_dir, f"{uuid_}.dat")

            if not os.path.isfile(file):
                raise NotImplementedError("Player creation hasn't been implemented yet...")

            async with aiofile.async_open(file, "rb") as player_file:
                player = Player.from_nbt(nbt.TAG_Compound.unpack(Buffer(await player_file.read())))

                self.cache[int(uuid_)] = player

                return player
