from jwt import InvalidTokenError
from config import config
from cachetools import TTLCache
from secure_uuid import secure_uuid
import time
import jwt
import os

SECRET = config.jwt_secret
TG_LINK_CACHE = TTLCache(maxsize=16384, ttl=60*5) # 5 min
SIGNIN_TOKENS_CACHE = TTLCache(maxsize=16384, ttl=60*5) # 5 min

class MinUserInfo:
    user_id: int
    username: str
    is_admin: bool

    def __init__(self, user_id: int, username: str, is_admin: bool):
        self.user_id = user_id
        self.username = username
        self.is_admin = is_admin


def encode_user_in_jwt(user: MinUserInfo, exp: time.time) -> str:
    return jwt.encode(
        dict(user_id=user.user_id, username=user.username, is_admin=user.is_admin, exp=exp),
        key=SECRET,
        algorithm="HS256"
    )


def get_user_from_jwt(jwt_token: str) -> MinUserInfo:
    """
    :raises:
        InvalidTokenError
    """
    dd = jwt.decode(jwt_token, key=SECRET, algorithms=["HS256"])
    return MinUserInfo(
        user_id=dd["user_id"],
        username=dd["username"],
        is_admin=dd["is_admin"],
    )

def get_link_token_for_tg(user: MinUserInfo) -> str:
    link_token = os.urandom(16).hex()
    TG_LINK_CACHE[user.user_id] = link_token
    return f'{link_token}_{user.user_id}'

def get_user_id_by_tg_link_token(link_token: str) -> int:
    link_token, user_id = link_token.split('_')
    user_id = int(user_id)
    link_token_from_cache = TG_LINK_CACHE[user_id]
    if link_token == link_token_from_cache:
        return user_id
    else:
        raise InvalidTokenError


def create_signin_token_for_user(user: MinUserInfo) -> str:
    token = secure_uuid(user.username).encode('utf-8').hex()

    SIGNIN_TOKENS_CACHE[token] = user

    return token

def get_auth_token_by_signin_token(signin_token: str, exp: time.time) -> str:
    if not signin_token in SIGNIN_TOKENS_CACHE:
        raise InvalidTokenError

    user = SIGNIN_TOKENS_CACHE[signin_token]

    return jwt.encode(
        dict(user_id=user.user_id, username=user.username, is_admin=user.is_admin, exp=exp),
        key=SECRET,
        algorithm="HS256"
    )