import hashlib

def get_sha256_hash(string):
    bytes = string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(bytes)
    hash_bytes = sha256_hash.digest()
    return hash_bytes.hex()
