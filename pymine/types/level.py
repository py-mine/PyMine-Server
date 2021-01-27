import pymine.types.nbt as nbt


class LevelData:
    def __init__(self, data: nbt.TAG) -> None:
        self.data = data
        self.allow_commands = data
