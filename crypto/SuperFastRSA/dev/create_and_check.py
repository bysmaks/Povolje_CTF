from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
from functools import reduce
import gmpy2

N=224545154741494280023620141096515237125248079646047213969438921487459681991296055040528145526560910256798778271668325297683345486253133747849362112475217815925133678041527020152841127174181678929695131286340633430882984010012128637176410468635268445836038764189299135645760371142503539978298425350632846703040382919781191126784931639702656589962469374511460395738996096049952080644866130024778837379533210292803385256853328378919395721430245073714881850720383389919752701115089266381706592487155194744140991776347066238076647871531475698709600981928732390837430547062480981639714187487045487009439291456911577311443969232904365981422062364743708688949658621759934657010113075196739160041601248980105996986563517253751484461
P=N # N=p*q, q=1
E=65537 

# Generate the private key
key = RSA.construct((N,E))
publickey = key.publickey()
public = key.publickey().exportKey('PEM')
open('public.pem', 'wb').write(public)

# Encrypt the message
plaintext="Not so secure, right? flags ctf{n3w_w34k_4lg0r1thm}"

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

# Convert the message to numeric type 
text2int=text2Int(plaintext)
print(f"Plaintext (numeric type): {text2int}")
plaintext=int2Text(text2int,1024)
print(f"Plaintext (string type): {plaintext}")

# Encrypt the message
messageEnc=encrypt(text2Int(plaintext),N,E)
print(f"Encrypted message (numeric type): {messageEnc}")
messageToBase64=b64encode(messageEnc.to_bytes(512, byteorder='big'))
print(f"Encrypted message (base64 type): {messageToBase64}")
open('flag.enc', 'wb').write(messageToBase64)

# Decrypt the message
D = gmpy2.invert(E, (P-1)) # Euler's totient function, but if q=1, then phi(n) = p-1
print(f"Private exponent: {D}")
messageEnc = b64decode(open("flag.enc").read().encode('utf-8'))
messageEnc = int.from_bytes(messageEnc, byteorder='big')
decryptMessage=encrypt(messageEnc,N,D)
print(f"Decrypted message (numeric): {decryptMessage}")
messagePlaintext = int2Text(decryptMessage,1024)
print(f"Decrypted message (string): {messagePlaintext}")
