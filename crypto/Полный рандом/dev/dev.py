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
flag = "ctf{cypher_is_weak_very_sad}"
key = bytearray(random.getrandbits(8) for _ in range(len(flag)))
print(encypt(key, flag))
#[151, 376, 187, 190, 204, 304, 194, 292, 117, 158, 179, 464, 214, 298, 107, 334, 274, 115, 192, 250, 140, 254, 498, 151, 164, 506, 186, 190, 370, 200, 454, 234, 286]