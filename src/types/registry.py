from src.util.immutable import make_immutable

class Registry:
    def __init__(self, data: dict):
        self.data = make_immutable({k: v['protocol_id'] for k, v in data.items()})
        self.data_reversed = make_immutable({v: k for k, v in data.items()})

    def encode(self, key: object) -> object:
        return self.data[key]

    def decode(self, value: object) -> object:
        return self.data_reversed[value]
