
PACKET_HANDLERS = {'handshaking': {}, 'login': {}, 'play': {}, 'status': {}}


# Decorator for adding a coroutine to handle a specific incoming packet
def handle_packet(state: str, id_: int):
    def command_deco(func):
        try:
            PACKET_HANDLERS[state][id_].append(func)
        except KeyError:
            PACKET_HANDLERS[state][id_] = [func]

        return func

    return command_deco
