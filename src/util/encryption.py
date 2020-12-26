import hashlib

__all__ = ('generate_verify_hash',)


def generate_verify_hash(shared_secret, public_key):
    verify_hash = hashlib.sha1()

    verify_hash.update((' '*20).encode('utf-8'))
    verify_hash.update(shared_secret)
    verify_hash.update(public_key)

    return int.from_bytes(verify_hash.digest(), byteorder='big', signed=True)
