from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from asyncio import StreamReader, StreamWriter
import aiohttp
import uuid

from src.api import handle_packet

from src.util.encryption import *
from src.util.share import share

from src.types.packet import Packet
from src.types.buffer import Buffer

from src.types.packets.login.set_comp import LoginSetCompression
from src.types.packets.login.login import *

login_cache = {}
states = share['states']


@handle_packet('login', 0x00)
async def login_start(r: 'StreamReader', w: 'StreamWriter', packet: Packet, remote: tuple) -> tuple:
    if share['conf']['online_mode']:  # Online mode is enabled, so we request encryption
        lc = login_cache[remote] = {'username': packet.username, 'verify': None}

        packet = LoginEncryptionRequest(
            share['rsa']['public'].public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

        lc['verify'] = packet.verify_token

        w.write(Buffer.pack_packet(packet))
        await w.drain()
    else:  # No need for encryption since online mode is off, just send login success
        uuid_ = uuid.uuid4()  # This should be only generated if the player name isn't found in the world data, but no way to do that rn

        w.write(Buffer.pack_packet(LoginSuccess(uuid_, packet.username), share['comp_thresh']))
        await w.drain()

        states[remote] = 3  # Update state to play

    return True, r, w


@handle_packet('login', 0x01)
async def encrypted_login(r: 'StreamReader', w: 'StreamWriter', packet: Packet, remote: tuple) -> tuple:
    shared_key, auth = await server_auth(packet, remote, login_cache[remote])

    del login_cache[remote]  # No longer needed

    if not auth:  # If authentication failed, disconnect client
        w.write(Buffer.pack_packet(LoginDisconnect('Failed to authenticate your connection.')))
        await w.drain()
        return False, r, w

    # Generate a cipher for that client using the shared key from the client
    cipher = gen_aes_cipher(shared_key)

    # Replace streams with ones which auto decrypt + encrypt data when reading/writing
    r = EncryptedStreamReader(r, cipher.decryptor())
    w = EncryptedStreamWriter(w, cipher.encryptor())

    if share['comp_thresh'] > 0:  # Send set compression packet if needed
        w.write(Buffer.pack_packet(LoginSetCompression(share['comp_thresh'])))
        await w.drain()

    # Send LoginSuccess packet, tells client they've logged in succesfully
    w.write(Buffer.pack_packet(LoginSuccess(*auth), share['comp_thresh']))
    await w.drain()

    return True, r, w


# Verifies that the shared key and token are the same, and does other authentication methods
# Returns the decrypted shared key and the client's username and uuid
async def server_auth(packet: 'LoginEncryptionResponse', remote: tuple, cache: dict) -> tuple:
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
            return decrypted_shared_key, (uuid.UUID(jj['id']), jj['name'],)

    return False, False
