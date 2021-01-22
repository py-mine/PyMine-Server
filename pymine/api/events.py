import asyncio


class EventHandlers:
    def __init__(self, server):
        self.server = server

        self.must_be_coroutine = "Decorated object must be a coroutine function"

        self._packet = {"handshaking": {}, "login": {}, "play": {}, "status": {}}
        self._server_ready = []
        self._server_stop = []

    def on_packet(self, state: str, id_: int):
        def command_deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError(self.must_be_coroutine)

            try:
                self._packet[state][id_].append(func)
            except KeyError:
                self._packet[state][id_] = [func]

            return func

        return command_deco

    def on_server_ready(self, func):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError(self.must_be_coroutine)

        self._server_ready.append(func)

        return func

    def on_server_stop(self, func):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError(self.must_be_coroutine)

        self._server_stop.append(func)

        return func
