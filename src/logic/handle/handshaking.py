import asyncio

from src.api import handle_packet

from src.util.share import share


@handle_packet('handshaking', 0x00)
async def handshake(r: 'StreamReader', w: 'StreamWriter', packet: Packet, remote: tuple) -> tuple:
    share['states'][remote] = packet.next_state
