from pymine.api.abc import AbstractWorldGenerator


class Register:
    def __init__(self) -> None:
        self._generators = {}

    def world_generator(self, name: str):
        def deco(cls):
            if not issubclass(cls, AbstractWorldGenerator):
                raise ValueError(f"Decorated class must be a subclass of AbstractWorldGenerator")

            self._generators[name] = cls

            return cls

        return deco
