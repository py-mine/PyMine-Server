from cryptography.hazmat.primitives.asymmetric import rsa
import aiohttp

from src.types.packets.login.login import *
from src.types.buffer import Buffer

async def request_encryption(r: 'StreamReader', w: 'StreamWriter', packet: 'LoginStart'):
    w.write(Buffer.pack_packet(LoginEncryptionRequest()))
