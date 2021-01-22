import asyncio


class EventsHandler:
    def __init__(self, server):
        self.server = server

        self._packet = {"handshaking": {}, "login": {}, "play": {}, "status": {}}
        self._server_ready = []
        self._server_stop = []

    def on_packet(self, state: str, id_: int):
        def command_deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError("Decorated object must be a coroutine function")

            try:
                self._packet[state][id_].append(func)
            except KeyError:
                self._packet[state][id_] = [func]

            return func

        return command_deco
