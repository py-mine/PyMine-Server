from asyncio import StreamReader, StreamWriter

from pymine.api.packet import handle_packet
from pymine.util.share import share

from pymine.types.packet import Packet


@handle_packet('handshaking', 0x00)
async def handshake(r: 'StreamReader', w: 'StreamWriter', packet: Packet, remote: tuple) -> tuple:
    share['states'][remote] = packet.next_state
    return True, r, w
