# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import aiofile
import struct
import uuid
import time
import os

from pymine.types.player import Player
from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class PlayerDataIO:
    def __init__(self, server, level_name: str):
        self.server = server
        self.level_name = level_name

        self.data_dir = os.path.join("worlds", level_name, "playerdata")

        self.cache = {}

    # Fetch a player by their uuid, this is cached to avoid duplicate Player objects and de-synced saving (possible future problem)
    async def fetch_player(self, uuid_: uuid.UUID) -> Player:
        try:
            return self.cache[int(uuid_)]
        except KeyError:
            file = os.path.join(self.data_dir, f"{uuid_}.dat")  # filename of the player

            if not os.path.isfile(file):  # create new player if needed
                level_data = self.server.worlds["minecraft:overworld"].data

                player = Player.new(
                    self.server.api.eid(),
                    uuid_,
                    (level_data["SpawnX"], level_data["SpawnY"], level_data["SpawnX"]),
                    "minecraft:overworld",
                )
                self.cache[int(player.uuid)] = player

                return player

            async with aiofile.async_open(file, "rb") as player_file:  # load preexisting
                player = Player(self.server.eid(), nbt.TAG_Compound.unpack(Buffer(await player_file.read())))
                self.cache[player.uuid] = player

                return player
