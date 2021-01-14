import asyncio

SERVER_READY_HANDLERS = []
SERVER_STOP_HANDLERS = []


def on_server_ready(func):
    if not asyncio.iscoroutinefunction(func):
        raise ValueError('Decorated object must be a coroutine function')

    SERVER_READY_HANDLERS.append(func)

    return func


def on_server_stop(func):
    if not asyncio.iscoroutinefunction(func):
        raise ValueError('Decorated object must be a coroutine function')

    SERVER_STOP_HANDLERS.append(func)

    return func
