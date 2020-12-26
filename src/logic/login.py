from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import aiohttp
import uuid

from src.types.packets.login.login import *
from src.types.buffer import Buffer

from src.util.encryption import *

# https://github.com/ammaraskar/pyCraft/blob/master/minecraft/networking/encryption.py


async def request_encryption(r: 'StreamReader', w: 'StreamWriter', packet: 'LoginStart', share: dict):
    w.write(Buffer.pack_packet(LoginEncryptionRequest(
        share['rsa']['public'].public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )))

    await w.drain()


async def server_auth(packet: 'LoginEncryptionResponse', remote: tuple, username: str, share: dict):
    resp = await share['ses'].get(
        'https://sessionserver.mojang.com/session/minecraft/hasJoined?username=username&serverId=hash',
        params={
            'username': username,
            'serverId': generate_verify_hash(
                packet.shared_key,
                share['rsa']['public'].public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
        }
    )

    jj = await resp.json()

    return uuid.UUID(jj['id']), jj['name']


async def login_success(r: 'StreamReader', w: 'StreamWriter', username: str, uuid_: uuid.UUID = None, share: dict):  # nopep8
    if uuid_ is None:
        resp = await share['ses'].get(f'https://api.mojang.com/users/profiles/minecraft/{player}')
        jj = await resp.json()
        uuid_ = uuid.UUID(jj['id'])

    w.write(Buffer.pack_packet(LoginSuccess(uuid_, username)))
    await w.drain()
