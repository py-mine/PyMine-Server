
PLAYER_JOIN_HANDLERS = []
PLAYER_LEAVE_HANDLERS = []

def on_player_join(func):
    PLAYER_JOIN_HANDLERS.append(func)

    return func


def on_player_leave(func):
    PLAYER_LEAVE_HANDLERS.append(func)

    return func
