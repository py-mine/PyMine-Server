from pymine.types.packet import Packet
from pymine.types.stream import Stream

from pymine.api.packet import handle_packet
from pymine.util.share import share


@handle_packet("handshaking", 0x00)
async def handshake(stream: Stream, packet: Packet) -> tuple:
    share["states"][stream.remote] = packet.next_state
    return True, stream
