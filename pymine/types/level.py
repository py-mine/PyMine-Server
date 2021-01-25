import nbt

class LevelData:
    def __init__(data: nbt.TAG) -> None:
        self.data = data
        self.allow_commands = data
