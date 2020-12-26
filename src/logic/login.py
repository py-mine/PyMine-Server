from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import aiohttp

from src.types.packets.login.login import *
from src.types.buffer import Buffer

ses = aiohttp.ClientSession()


async def request_encryption(r: 'StreamReader', w: 'StreamWriter', packet: 'LoginStart', share: dict):
    w.write(Buffer.pack_packet(LoginEncryptionRequest(
        share['public_key'].public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )))

    await w.drain()
