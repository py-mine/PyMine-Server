import asyncio

from pymine.data.states import STATES


class EventHandler:
    def __init__(self):
        self.must_be_coroutine = "Decorated object must be a coroutine function."

        # handshaking, login, play, status
        self._packet = ({}, {}, {}, {})
        self._server_ready = []  # [func, func, func,..]
        self._server_stop = []  # [func, func, func,..]

    def on_packet(self, state: str, id_: int):
        state = STATES.encode(state)

        def deco(func):
            if not asyncio.iscoroutinefunction(func):
                raise ValueError(self.must_be_coroutine)

            try:
                self._packet[state][id_].append(func)
            except KeyError:
                self._packet[state][id_] = [func]

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
