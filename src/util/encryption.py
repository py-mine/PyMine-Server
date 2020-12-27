from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib

__all__ = ('gen_verify_hash', 'gen_aes_cipher',)


def gen_verify_hash(shared_secret: bytes, public_key: bytes):
    verify_hash = hashlib.sha1()

    verify_hash.update((' ' * 20).encode('utf-8'))
    verify_hash.update(shared_secret)
    verify_hash.update(public_key)

    return format(int.from_bytes(verify_hash.digest(), byteorder='big', signed=True), 'x')


def gen_aes_cipher(shared_secret: bytes):
    return Cipher(
        algorithms.AES(shared_secret),
        modes.CFB8(shared_secret)
    )
