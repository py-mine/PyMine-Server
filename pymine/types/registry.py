from immutables import Map

from pymine.util.immutable import make_immutable


class Registry:
    def __init__(self, data: object):
        if isinstance(data, (dict, Map)):
            self.data = make_immutable({k: v['protocol_id'] for k, v in data.items()})
            self.data_reversed = make_immutable({v: k for k, v in data.items()})
        elif isinstance(data, (list, tuple)):
            self.data = data
            self.data_reversed = make_immutable({v: i for i, v in enumerate(data)})
        else:
            raise Exception(
                'Creating a registry from something other than a dict, Map, tuple, or list is unsupported'
            )

    def encode(self, key: object) -> object:
        return self.data[key]

    def decode(self, value: object) -> object:
        return self.data_reversed[value]
