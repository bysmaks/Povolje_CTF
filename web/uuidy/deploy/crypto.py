import hashlib
import os
from config import config

def hash_password(password: str) -> str:
    hashed = hashlib.sha256((config.jwt_secret + password).encode('utf-8')).digest()
    return hashed.hex()

def check_password(stored_hash: str, password: str) -> bool:
    hashed = bytes.fromhex(stored_hash)
    password_hash = hashlib.sha256((config.jwt_secret + password).encode('utf-8')).digest()
    return password_hash == hashed
