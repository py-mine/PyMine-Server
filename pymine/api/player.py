import asyncio

PLAYER_JOIN_HANDLERS = []
PLAYER_LEAVE_HANDLERS = []


def on_player_join(func):
    if not asyncio.iscoroutinefunction(func):
        raise ValueError('Decorated object must be a coroutine function')

    PLAYER_JOIN_HANDLERS.append(func)

    return func


def on_player_leave(func):
    if not asyncio.iscoroutinefunction(func):
        raise ValueError('Decorated object must be a coroutine function')

    PLAYER_LEAVE_HANDLERS.append(func)

    return func
