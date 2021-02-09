from immutables import Map

from pymine.util.immutable import make_immutable


class Registry:
    def __init__(self, data: object, data_reversed: object = None) -> None:
        self.data_reversed = data_reversed

        if isinstance(data, (dict, Map)):
            self.data = make_immutable(data)

            if data_reversed is None:
                self.data_reversed = make_immutable({v: k for k, v in data.items()})
        elif isinstance(data, (list, tuple)):
            self.data_reversed = data
            self.data = make_immutable({v: i for i, v in enumerate(self.data_reversed)})
        else:
            raise TypeError("Creating a registry from something other than a dict, Map, tuple, or list isn't supported")

    def encode(self, key: object) -> object:  # most likely an identifier to an int
        return self.data[key]

    def decode(self, value: object) -> object:  # most likely a numeric id to a string identifier
        return self.data_reversed[value]
