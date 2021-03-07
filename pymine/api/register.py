from pymine.api.abc import AbstractWorldGenerator


class Register:
    def __init__(self) -> None:
        self._plugins = {}
        self._generators = {}

    def world_generator(self, name: str):
        def deco(cls):
            if not issubclass(cls, AbstractWorldGenerator):
                raise ValueError(f"Decorated class must be a subclass of AbstractWorldGenerator")

            self._generators[name] = cls

            return cls

        return deco

    def plugin(self, plugin: AbstractPlugin) -> None:
        if not isinstance(plugin, AbstractPlugin):
            raise ValueError("Plugin must be an instance of AbstractPlugin.")

        self._plugins[plugin.__name__] = plugin
