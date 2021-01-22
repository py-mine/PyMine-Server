import asyncio

from pymine import server


def on_packet(state: str, id_: int):
    def command_deco(func):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Decorated object must be a coroutine function")

        try:
            server.api.handlers.packet[state][id_].append(func)
        except KeyError:
            server.api.handlers.packet[state][id_] = [func]

        return func

    return command_deco
