from pymine.types.packet import Packet
from pymine.types.stream import Stream

from pymine.server import server


@server.api.events.on_packet("play", 0x0B)
async def plugin_message_recv(stream: Stream, packet: Packet) -> None:
    if packet.channel == "minecraft:brand":
        server.cache.uuid[stream.remote].brand = packet.data.unpack_string()
