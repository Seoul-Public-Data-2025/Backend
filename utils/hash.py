import hashlib
import base64

def hash_uid(uid: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(uid.encode('utf-8'))
    hash_bytes = sha256.digest()
    base64_encoded = base64.b64encode(hash_bytes).decode('utf-8')
    return base64_encoded