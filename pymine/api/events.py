import asyncio


class EventHandlers:
    def __init__(self, server):
        self.server = server

        self.must_be_coroutine = "Decorated object must be a coroutine function."

        self._packet = {"handshaking": {}, "login": {}, "play": {}, "status": {}}
        self._server_ready = []
        self._server_stop = []
        self._commands = {}  # {name: (func, node)}

    def on_packet(self, state: str, id_: int):
        def deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError(self.must_be_coroutine)

            try:
                self._packet[state][id_].append(func)
            except KeyError:
                self._packet[state][id_] = [func]

            return func

        return deco

    def on_command(self, name: str, node: str):
        if name in self._commands:
            raise ValueError("Command name is already in use.")

        if " " in name:
            raise ValueError("Command name may not contain spaces.")

        def deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError(self.must_be_coroutine)

            self._commands[name] = func, node
            return func

        return deco

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
