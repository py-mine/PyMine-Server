import uuid
import os

from pymine.types.buffer import Buffer
from pymine.types.player import Player
import pymine.types.nbt as nbt


def fetch_player(level_name: str, uuid_: uuid.UUID) -> None:
    playerdata_dir = os.path.join("worlds", level_name, "playerdata")

    uuid_ = str(uuid_)
    file = os.path.join(playerdata_dir, uuid_ + ".dat")

    if not os.path.isfile(file):
        raise NotImplementedError("Player creation hasn't been implemented yet...")

    with open(file, "rb") as f:
        return Player(nbt.TAG_Compound.unpack(Buffer(f.read())))
