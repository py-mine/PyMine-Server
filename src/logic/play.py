from src.types.packets.play import player as packets_player
from src.types.buffer import Buffer

from src.util.share import share, logger


async def play(r: 'StreamReader', w: 'StreamWriter', packet: 'Packet', remote: tuple) -> tuple:
    pass


async def finish_login(r: 'StreamReader', w: 'StreamWriter', remote: tuple) -> None:
    w.write(Buffer.pack_packet(packets_player.PlayJoinGame(

    )))

    await w.drain()
