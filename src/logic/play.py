from src.types.buffer import Buffer

from src.util.share import share, logger


async def play(r: 'StreamReader', w: 'StreamWriter', packet: 'Packet', remote: tuple):
    
