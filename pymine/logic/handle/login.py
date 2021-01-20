from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import aiohttp
import uuid

from pymine.api.packet import handle_packet

import pymine.util.encryption as encryption
from pymine.util.share import share

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.stream import Stream

from pymine.types.packets.login.set_comp import LoginSetCompression
import pymine.types.packets.login.login as login_packets

login_cache = {}
states = share['states']


@handle_packet('login', 0x00)
async def login_start(stream: Stream, packet: Packet) -> tuple:
    if share['conf']['online_mode']:  # Online mode is enabled, so we request encryption
        lc = login_cache[stream.remote] = {'username': packet.username, 'verify': None}

        packet = login_packets.LoginEncryptionRequest(
            share['rsa']['public'].public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

        lc['verify'] = packet.verify_token

        stream.write(Buffer.pack_packet(packet))
        await stream.drain()
    else:  # No need for encryption since online mode is off, just send login success
        uuid_ = uuid.uuid4()  # This should be only generated if the player name isn't found in the world data, but no way to do that rn

        stream.write(Buffer.pack_packet(login_packets.LoginSuccess(uuid_, packet.username), share['comp_thresh']))
        await stream.drain()

        states[stream.remote] = 3  # Update state to play

    return True, stream


@handle_packet('login', 0x01)
async def encrypted_login(stream: Stream, packet: Packet) -> tuple:
    shared_key, auth = await server_auth(packet, stream.remote, login_cache[stream.remote])

    del login_cache[remote]  # No longer needed

    if not auth:  # If authentication failed, disconnect client
        stream.write(Buffer.pack_packet(login_packets.LoginDisconnect('Failed to authenticate your connection.')))
        await stream.drain()
        return False, stream

    # Generate a cipher for that client using the shared key from the client
    cipher = encryption.gen_aes_cipher(shared_key)

    # Replace streams with ones which auto decrypt + encrypt data when reading/writing
    r = encryption.EncryptedStreamReader(r, cipher.decryptor())
    w = encryption.EncryptedStreamWriter(w, cipher.encryptor())

    if share['comp_thresh'] > 0:  # Send set compression packet if needed
        stream.write(Buffer.pack_packet(LoginSetCompression(share['comp_thresh'])))
        await stream.drain()

    # Send LoginSuccess packet, tells client they've logged in succesfully
    stream.write(Buffer.pack_packet(login_packets.LoginSuccess(*auth), share['comp_thresh']))
    await stream.drain()

    return True, stream


# Verifies that the shared key and token are the same, and does other authentication methods
# Returns the decrypted shared key and the client's username and uuid
async def server_auth(packet: login_packets.LoginEncryptionResponse, remote: tuple, cache: dict) -> tuple:
    if share['rsa']['private'].decrypt(packet.verify_token, PKCS1v15()) == cache['verify']:
        decrypted_shared_key = share['rsa']['private'].decrypt(packet.shared_key, PKCS1v15())

        resp = await share['ses'].get(
            'https://sessionserver.mojang.com/session/minecraft/hasJoined',
            params={
                'username': cache['username'],
                'serverId': encryption.gen_verify_hash(
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
