from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import aiohttp

from src.types.packets.login.login import *
from src.types.buffer import Buffer

from src.util.encryption import *

# https://github.com/ammaraskar/pyCraft/blob/master/minecraft/networking/encryption.py

ses = aiohttp.ClientSession()


async def request_encryption(r: 'StreamReader', w: 'StreamWriter', packet: 'LoginStart', share: dict):
    w.write(Buffer.pack_packet(LoginEncryptionRequest(
        share['public_key'].public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )))

    await w.drain()


async def server_auth(packet: 'LoginEncryptionResponse', remote: tuple, username: str, share: dict):
    resp = await ses.get(
        'https://sessionserver.mojang.com/session/minecraft/hasJoined?username=username&serverId=hash',
        params={
            'username': username,
            'serverId': generate_verify_hash(
                packet.shared_key,
                share['public_key'].public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
        }
    )

    return uuid.UUID(resp['id']), resp['name']


async def login_success(r: 'StreamReader', w: 'StreamWriter', uuid: 'uuid.UUID', username: str):
    w.write(Buffer.pack_packet(LoginSuccess(uuid, username)))
    await w.drain()
