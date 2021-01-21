from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib
import asyncio

__all__ = (
    "gen_rsa_keys",
    "gen_verify_hash",
    "gen_aes_cipher",
)


def gen_rsa_keys():
    private_key = rsa.generate_private_key(65537, 1024)

    return private_key, private_key.public_key()


def gen_verify_hash(shared_key: bytes, public_key: bytes):
    verify_hash = hashlib.sha1()

    verify_hash.update((" " * 20).encode("utf-8"))
    verify_hash.update(shared_key)
    verify_hash.update(public_key)

    return format(int.from_bytes(verify_hash.digest(), byteorder="big", signed=True), "x")


def gen_aes_cipher(shared_key: bytes):
    return Cipher(algorithms.AES(shared_key), modes.CFB8(shared_key))
