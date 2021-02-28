from pymine.types.packet import Packet
from pymine.types.stream import Stream

from pymine.net.packets.play.player import PlayDisconnect

from pymine.server import server


@server.api.events.on_packet("play", 0x00)
async def on_teleport_confirm(stream: Stream, packet: Packet) -> None:
    player = await server.playerio.fetch_player(server.cache.uuid[stream.remote])

    if player.teleport_id != packet.teleport_id:
        await server.send_packet(stream, PlayDisconnect(f"Invalid teleport ID ({repr(player.teleport_id)} != {repr(packet.teleport_id)})."))
