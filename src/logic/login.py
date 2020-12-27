from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import aiohttp
import uuid

from src.types.packets.login.set_comp import LoginSetCompression
from src.types.packets.login.login import *
from src.types.buffer import Buffer

from src.util.encryption import *
from src.util.share import share

# https://github.com/ammaraskar/pyCraft/blob/master/minecraft/networking/encryption.py


async def request_encryption(r: 'StreamReader', w: 'StreamWriter', packet: 'LoginStart', lc: dict):
    packet = LoginEncryptionRequest(
        share['rsa']['public'].public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

    lc['verify'] = packet.verify_token

    w.write(Buffer.pack_packet(packet))
    await w.drain()


async def server_auth(packet: 'LoginEncryptionResponse', remote: tuple, cache: dict):
    if share['rsa']['private'].decrypt(packet.verify_token, PKCS1v15()) == cache['verify']:
        decrypted_shared_key = share['rsa']['private'].decrypt(packet.shared_key, PKCS1v15())

        resp = await share['ses'].get(
            'https://sessionserver.mojang.com/session/minecraft/hasJoined',
            params={
                'username': cache['username'],
                'serverId': gen_verify_hash(
                    decrypted_shared_key,
                    share['rsa']['public'].public_bytes(
                        encoding=serialization.Encoding.DER,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                )
            }
        )

        jj = await resp.json()

        if jj is not None:
            uuid_, name = uuid.UUID(jj['id']), jj['name']

            return decrypted_shared_key, (name, uuid_,)

    return False


async def set_compression(w, comp_thresh: int = -1):
    w.write(LoginSetCompression(comp_thresh))
    await w.drain()


async def login_success(r: 'StreamReader', w: 'StreamWriter', username: str, uuid_: uuid.UUID = None):  # nopep8
    if uuid_ is None:
        resp = await share['ses'].get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        jj = await resp.json()
        uuid_ = uuid.UUID(jj['id'])

    w.write(Buffer.pack_packet(LoginSuccess(uuid_, username)))
    await w.drain()


async def login_kick(w: 'StreamWriter'):
    w.write(Buffer.pack_packet(
        LoginKick('Failed to authenticate your connection.')
    ))
    await w.drain()
