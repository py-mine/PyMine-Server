import asyncio


class EventHandlers:
    def __init__(self, server):
        self.server = server

    def on_packet(self, state: str, id_: int):
        def command_deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError("Decorated object must be a coroutine function")

            try:
                self.server.api.handlers.packet[state][id_].append(func)
            except KeyError:
                self.server.api.handlers.packet[state][id_] = [func]

            return func

        return command_deco
