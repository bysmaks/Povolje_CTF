import time
import random

def encypt(key, message):
    encrypted = []
    for i in range(len(message)):
        if key[i] > ord(message[i]):
            encrypted.append((key[i] - ord(message[i])) ^ (key[i] + ord(message[i])))
        else:
            encrypted.append(key[i] + ord(message[i]))
    return encrypted

random.seed(int(time.time()))
flag = "ctf{redacted}"
key = bytearray(random.getrandbits(8) for _ in range(len(flag)))
print(encypt(key, flag))
#[218, 224, 182, 203, 334, 246, 352, 172, 314, 134, 179, 168, 161, 462, 278, 202, 194, 160, 322, 244, 458, 138, 232, 125, 362, 138, 115, 382]