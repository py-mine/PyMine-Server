from pymine.api.abc import AbstractWorldGenerator, AbstractPlugin

from pymine.data.states import STATES


class Register:
    def __init__(self) -> None:
        self._plugins = {}

        self._generators = {}

        self._on_packet = ({}, {}, {}, {})  # handshaking, login, play, status

    def plugin(self, plugin: AbstractPlugin) -> None:
        if not isinstance(plugin, AbstractPlugin):
            raise ValueError("Plugin must be an instance of AbstractPlugin.")

        self._plugins[plugin.__name__] = plugin

    def world_generator(self, name: str):
        def deco(cls):
            if not issubclass(cls, AbstractWorldGenerator):
                raise ValueError(f"Decorated class must be a subclass of AbstractWorldGenerator")

            self._generators[name] = cls

            return cls

        return deco

    def on_packet(self, state: str, id_: int):
        state = STATES.encode(state)

        def deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError("Decorated object must be a coroutine function.")

            try:
                self._packet[state][id_].append(func)
            except KeyError:
                self._packet[state][id_] = [func]

            return func

        return deco
