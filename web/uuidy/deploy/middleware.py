from itsdangerous import SignatureExpired
from jwt import InvalidTokenError
from quart import redirect, request, url_for, g, make_response
from auth import get_user_from_jwt
from functools import wraps


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        g.is_authenticated = False

        if "auth" not in request.cookies:
            return redirect(url_for("signin"))

        auth_token = request.cookies["auth"]

        try:
            user = get_user_from_jwt(auth_token)
        except Exception:
            resp = await make_response(redirect(url_for("signin")))
            resp.delete_cookie("auth")
            return resp

        g.user = user
        g.is_authorized = True

        return await func(*args, **kwargs)
    return wrapper

def unlogin_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        g.is_authenticated = False

        if "auth" not in request.cookies:
            return await func(*args, **kwargs)

        auth_token = request.cookies["auth"]

        try:
            user = get_user_from_jwt(auth_token)
        except Exception:
            resp = await make_response(redirect(url_for("signin")))
            resp.delete_cookie("auth")
            return resp

        g.user = user
        g.is_authorized = True

        return redirect(url_for("notes"))
    return wrapper

def admin_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not g.is_authorized:
            return redirect(url_for("go_away"))

        if g.user is None or not g.user.is_admin:
            return redirect(url_for("go_away"))

        return await func(*args, **kwargs)
    return wrapper