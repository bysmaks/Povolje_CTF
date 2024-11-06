from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
from functools import reduce
import gmpy2

def int2Text(x,blocksize):
    text = "".join([chr((x >> j) & 0xff) for j in reversed(range(0, blocksize << 3, 8))])
    return text.lstrip("\x00")

def text2Int(text):
    return reduce(lambda x, y : (x << 8) + y, map(ord, text))

def encrypt(text,modulus,exponent):
    text=int(text)
    if text >= modulus:
        raise ValueError("Text too long")
    return pow(text,exponent,modulus)

# Get components from public key
publickey = RSA.importKey(open('public.pem').read())
N = publickey.n
E = publickey.e
P = N # N=p*q, q=1

# Decrypt the message
D = gmpy2.invert(E, (P-1)) # Euler's totient function, but if q=1, then phi(n) = p-1
print(f"Private exponent: {D}")
messageEnc = b64decode(open("flag.enc").read().encode('utf-8'))
messageEnc = int.from_bytes(messageEnc, byteorder='big')
decryptMessage=encrypt(messageEnc,N,D)
print(f"Decrypted message (numeric): {decryptMessage}")
messagePlaintext = int2Text(decryptMessage,1024)
print(f"Decrypted message (string): {messagePlaintext}")
