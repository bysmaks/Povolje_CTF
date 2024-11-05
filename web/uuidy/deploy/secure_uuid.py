from uuid import getnode
import time

MAC = getnode()
MAC_HEX = hex(MAC)[2:]
MAC_HEX_P1 = MAC_HEX[:len(MAC_HEX) // 2]
MAC_HEX_P2 = MAC_HEX[len(MAC_HEX) // 2:]

def secure_uuid(salt: str) -> str:
    salt = salt[:16].encode('utf-8').hex()
    t = int(time.time() * 10)
    timestamp_p_hex = hex(t)[2:]
    rand_hex = hex(int(((t * 1103515245 + 12345) / 65536) % 32768))[2:]
    return f"{MAC_HEX_P1}-{timestamp_p_hex}-{MAC_HEX_P2}-{rand_hex}-{salt}".upper()