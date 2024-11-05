from typing import Union
import asyncpg

class User:
    user_id: int
    username: str
    password_hash: str
    tg_chat_id: Union[int, None]
    is_admin: bool

    def __init__(self, user_id: int, username: str, password_hash: str, tg_chat_id: int, is_admin: bool):
        self.user_id = user_id
        self.username = username
        self.password_hash: str = password_hash
        self.tg_chat_id = tg_chat_id
        self.is_admin = is_admin

# TODO:
#   - [x] Перевести все методы на $1, $2
#   - [] Избавиться от всех f''

class DB:
    def __init__(self, ro_conn_pool: asyncpg.pool.Pool, rw_conn: asyncpg.pool.Pool):
        self.ro_conn = ro_conn_pool
        self.rw_conn = rw_conn

    async def create_user(self, username: str, password_hash: str, is_admin: bool = False) -> User:
        async with self.rw_conn.acquire() as con:
            result = await con.fetch(
                f"INSERT INTO users (username, password_hash, is_admin) "
                f"VALUES ($1, $2, $3) RETURNING user_id, username, password_hash, tg_chat_id, is_admin",
                username, password_hash, is_admin
            )

        return User(
            user_id=result[0][0],
            username=result[0][1],
            password_hash=result[0][2],
            tg_chat_id=result[0][3],
            is_admin=result[0][4]
        )

    async def get_user_by_username(self, username: str) -> Union[User, None]:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(
                f'SELECT user_id, username, password_hash, tg_chat_id, is_admin FROM users where username = $1',
                username)

        if len(result) == 0:
            return None

        return User(
            user_id=result[0][0],
            username=result[0][1],
            password_hash=result[0][2],
            tg_chat_id=result[0][3],
            is_admin=result[0][4]
        )

    async def get_user_by_user_id(self, user_id: int) -> User:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(
                f'SELECT user_id, username, password_hash, tg_chat_id, is_admin FROM users where user_id = $1', user_id)

        return User(
            user_id=result[0][0],
            username=result[0][1],
            password_hash=result[0][2],
            tg_chat_id=result[0][3],
            is_admin=result[0][4]
        )

    async def get_chat_id_by_user_id(self, user_id: int) -> int:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(f'SELECT tg_chat_id FROM users WHERE user_id = $1', user_id)

        return result[0][0]

    async def set_chat_id_by_user_id(self, user_id: int, chat_id: int):
        async with self.rw_conn.acquire() as con:
            await con.fetch(f'UPDATE users SET tg_chat_id = $1 WHERE user_id = $2', chat_id, user_id)

    async def get_notes_count(self, user_id: int) -> int:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(f'SELECT count(1) FROM notes WHERE user_id = $1', user_id)

        return result[0][0]

    async def new_note(self, user_id: int, content: str) -> int:
        async with self.rw_conn.acquire() as con:
            result = await con.fetch(
                f'INSERT INTO notes (user_id, content) VALUES ($1, $2) RETURNING note_id', user_id, content
            )

        return result[0][0]

    async def get_note_content(self, user_id: int, note_id: int) -> str:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(f'SELECT content FROM notes WHERE user_id = $1 AND note_id = $2', user_id, note_id)

        return result[0][0]

    async def get_user_notes(self, user_id: int) -> list[int]:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(f'SELECT note_id FROM notes WHERE user_id = $1', user_id)

        return [row[0] for row in result]

    async def get_user_notes_by_username(self, username: str) -> list[int]:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(f'SELECT note_id FROM notes n JOIN users u ON n.user_id = u.user_id WHERE u.username = $1', username)

        return [row[0] for row in result]

    async def get_user_note_content_by_username(self, username: str, note_id: int) -> list[int]:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(
                f'SELECT content FROM notes n JOIN users u ON n.user_id = u.user_id WHERE u.username = $1 AND note_id = $2',
                username, note_id
            )

        return result[0][0]

    async def get_users_count(self) -> int:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(f'SELECT count(1) FROM users')

        return result[0][0]

    async def get_users(self, limit: int, offset: int) -> list[User]:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(
                f'SELECT user_id, username, is_admin FROM users ORDER BY user_id LIMIT $1 OFFSET $2', limit, offset
            )

        return [User(user_id=row[0], username=row[1], is_admin=row[2], password_hash='', tg_chat_id=0) for row in result]

    async def is_user_exists(self, username: str) -> bool:
        async with self.ro_conn.acquire() as con:
            result = await con.fetch(f"SELECT EXISTS ( SELECT user_id FROM users WHERE username = '{username}' )")

        return result[0][0]
