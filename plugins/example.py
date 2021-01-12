from src.api import handle_packet


@handle_packet('handshaking', 0x00)
async def example_handle_handshake(r, w, packet, remote):
    print('Hello this is the example packet handler speaking how may I take your order sir')
