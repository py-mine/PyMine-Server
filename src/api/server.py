
SERVER_READY_HANDLERS = []
SERVER_STOP_HANDLERS = []


def on_server_ready(func):
    SERVER_READY_HANDLERS.append(func)

    return func


def on_server_stop(func):
    SERVER_STOP_HANDLERS.append(func)

    return func
