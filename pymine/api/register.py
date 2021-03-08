import asyncio

from pymine.api.abc import AbstractWorldGenerator, AbstractPlugin
from pymine.api.events import PacketEvent, ServerStartEvent

from pymine.data.states import STATES


class Register:
    def __init__(self) -> None:
        self._plugins = {}  # {}

        self._generators = {}  # world generators {name: object}

        # handshaking, login, play, status
        # (state, state, state, state)
        # {packet_id: {plugin_quali_name: event_object}}
        self._on_packet = ({}, {}, {}, {})

        # other events, {plugin_quali_name: event_object}
        self._on_server_start = {}

    def add_plugin(self, plugin: AbstractPlugin) -> None:
        if not isinstance(plugin, AbstractPlugin):
            raise ValueError("Plugin must be an instance of AbstractPlugin.")

        self._plugins[plugin.__name__] = plugin

    def add_world_generator(self, name: str):
        def deco(cls):
            if not issubclass(cls, AbstractWorldGenerator):
                raise ValueError(f"Decorated class must be a subclass of AbstractWorldGenerator")

            self._generators[name] = cls

            return cls

        return deco

    def on_packet(self, state: str, packet_id: int):
        state = STATES.encode(state)

        def deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError("Decorated object must be a coroutine function.")

            return PacketEvent(func, state, packet_id)

        return deco

    def on_server_start(self, func):
        return ServerStartEvent(func)
