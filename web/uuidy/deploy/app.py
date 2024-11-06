from typing import Union
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import decode_payload, create_start_link
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, ErrorEvent, InlineKeyboardMarkup, InlineKeyboardButton
from jwt import InvalidTokenError
from quart import Quart, render_template, request, url_for, redirect, make_response, g
from datetime import timedelta, datetime, timezone
from auth import MinUserInfo
from config import config
from crypto import hash_password, check_password
from db import DB
from middleware import login_required, admin_required, unlogin_required
import asyncpg, auth
import asyncio

app = Quart(__name__)
dp = Dispatcher()

db: Union[DB, None] = None
bot: Union[Bot, None] = None

TG_SIGNIN_LINK_PREFIX = f'http://{config.service_host}'
if config.use_https:
    TG_SIGNIN_LINK_PREFIX = TG_SIGNIN_LINK_PREFIX.replace('http', 'https')

MAX_NOTES_COUNT = 5

# TODO:
#   1. Вход по ссылке из ТГ+
#   2. Создание заметок
#   3. Админ панель

# TG BOT HANDLERS
@dp.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject):
    args = command.args
    payload = decode_payload(args)

    user_id = auth.get_user_id_by_tg_link_token(payload)

    user = await db.get_user_by_user_id(user_id=user_id)

    await db.set_chat_id_by_user_id(user_id=user_id, chat_id=message.chat.id)

    await message.answer(f"Вход через тг для аккаунта <b>{user.username}</b> настроен!")


@dp.error()
async def error_handler(event: ErrorEvent):
    print("critical error caused by", event.exception)
    if event.update is not None and event.update.message is not None:
        await event.update.message.reply("bad message or internal server error, idk)")


# HTTP HANDLERS
@app.before_serving
async def init_db():
    global db

    ro_pool = await asyncpg.create_pool(config.pg_ro_url)
    rw_pool = await asyncpg.create_pool(config.pg_rw_url)
    db = DB(ro_pool, rw_pool)

    try:
        # creating admin account
        password_hash = hash_password(config.admin_password)
        user = await db.create_user(username="admin", password_hash=password_hash, is_admin=True)
    except Exception as e:
        print("Can't create admin user:", e)


@app.before_serving
async def start_bot():
    global bot

    bot = Bot(token=config.tg_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.create_task(dp.start_polling(bot))
    print("tg bot started!")


@app.errorhandler(Exception)
async def handle_exception(e):
    print("got err:", e)
    if 'not found' in str(e).lower():
        return 'not found'

    return 'Bad request, internal server error, idk)', 500


@app.route("/")
@unlogin_required
async def index():
    return await render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
@unlogin_required
async def signup():
    if request.method == "POST":
        form = await request.form

        username: str = form["username"]
        password: str = form["password"]

        if len(username) == 0:
            return await render_template("signup.html", error="Юзернейм не может быть пустым")

        if not username.isalnum():
            return await render_template("signup.html", error="Юзернейм может содержать только буквы и цифры")

        if len(username) >= 256:
            return await render_template("signup.html", error="Юзернейм не должен быть длиннее 256 символов")

        if not 8 <= len(password) <= 128:
            return await render_template("signup.html", error="Пароль должен быть от 8 до 128 символов")

        try:
            password_hash = hash_password(password)
            user = await db.create_user(username, password_hash)
        except asyncpg.exceptions.UniqueViolationError:
            return await render_template("signup.html", error="username уже занят")
        except Exception as e:
            print(e)
            return await render_template("signup.html", error="Bad request or internal server error, idk)")

        auth_token = auth.encode_user_in_jwt(
            MinUserInfo(user_id=user.user_id, username=user.username, is_admin=user.is_admin),
            exp=datetime.now(timezone.utc) + timedelta(hours=8),
        )
        resp = await make_response(redirect(url_for("notes")))
        resp.set_cookie('auth', auth_token, max_age=60 * 60 * 24)

        return resp

    return await render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
@unlogin_required
async def signin():
    if request.method == "POST":
        form = await request.form

        username = form["username"]
        password = form["password"]

        try:
            user = await db.get_user_by_username(username)
        except Exception as e:
            return await render_template("signin.html", error="Что-то пошло не так")

        if user is None:
            return await render_template("signin.html", error="Неверный логин или пароль")

        if not check_password(user.password_hash, password):
            return await render_template("signin.html", error="Неверный логин или пароль")

        auth_token = auth.encode_user_in_jwt(
            MinUserInfo(user_id=user.user_id, username=user.username, is_admin=user.is_admin),
            exp=datetime.now(timezone.utc) + timedelta(hours=8),
        )

        resp = await make_response(redirect(url_for("notes")))
        resp.set_cookie('auth', auth_token, max_age=60 * 60 * 24)
        return resp

    return await render_template("signin.html")


@app.route("/settings", methods=["GET"])
@login_required
async def settings():
    chat_id = await db.get_chat_id_by_user_id(g.user.user_id)
    is_tg_connected = chat_id is not None

    return await render_template("settings.html", is_tg_connected=is_tg_connected)


@app.route('/link_tg', methods=["GET"])
@login_required
async def link_tg():
    user: MinUserInfo = g.user
    link_token = auth.get_link_token_for_tg(user)
    link = await create_start_link(bot, link_token, encode=True)
    return redirect(link)


@app.route('/tg_signin/<token>', methods=["GET"])
async def tg_signin(token: str):
    try:
        auth_token = auth.get_auth_token_by_signin_token(token, exp=datetime.now(timezone.utc) + timedelta(hours=8))
    except InvalidTokenError:
        return await render_template(
            "tg_signin.html",
            error="Вероятно ссылка уже протухла, попробуйте запросить новую"
        )

    resp = await make_response(redirect(url_for("notes")))
    resp.set_cookie('auth', auth_token, max_age=60 * 60 * 24)

    return resp


@app.route('/send_tg_link', methods=["GET", "POST"])
@unlogin_required
async def send_tg_link():
    if request.method == "POST":
        form = await request.form
        username = form["username"]

        if len(username) >= 256:
            return await render_template("tg_signin.html", error="Юзернейм не должен быть длиннее 256 символов")

        user = await db.get_user_by_username(username)
        if user is None:
            return await render_template(
                "tg_signin.html",
                error="У юзера не настроен вход через Telegram!"
            )

        signin_token = auth.create_signin_token_for_user(
            MinUserInfo(user_id=user.user_id, username=user.username, is_admin=user.is_admin)
        )
        signin_link = f'{TG_SIGNIN_LINK_PREFIX}/tg_signin/{signin_token}'

        if user.tg_chat_id is None:
            return await render_template(
                "tg_signin.html",
                error="У юзера не настроен вход через Telegram!"
            )

        button = InlineKeyboardButton(text="Войти", url=signin_link)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button], ])

        await bot.send_message(
            user.tg_chat_id,
            f'Для входа в аккаунт <b>{user.username}</b> нажмите на кнопку ниже, '
            f'либо перейдите по <a href="{signin_link}">ссылке</a>.\n\n'
            f'<i>Кнопка входа и ссылка перестанут работать через 5 минут.</i>',
            reply_markup=keyboard
        )

        return await render_template("tg_signin.html", success_message='Ссылка отправлена!')

    return await render_template("tg_signin.html")

@app.route("/notes")
@login_required
async def notes():
    notes_ids = await db.get_user_notes(g.user.user_id)
    return await render_template("notes.html", notes_ids=notes_ids)

@app.route("/new_note", methods=["GET", "POST"])
@login_required
async def new_note():
    if request.method == "POST":
        form = await request.form
        content = form["content"]

        content = content.strip()
        if len(content) == 0:
            return await render_template("new_note.html", error="Размер заметки не может быть меньше 1 символа")

        if len(content) > 1000:
            return await render_template("new_note.html", error="Размер заметки не может превышать 1000 символов")

        notes_count = await db.get_notes_count(user_id=g.user.user_id)
        if notes_count >= MAX_NOTES_COUNT:
            return await render_template("new_note.html", error=f"Нельзя создать больше {MAX_NOTES_COUNT} заметок")

        note_id = await db.new_note(user_id=g.user.user_id, content=content)

        return redirect(url_for("note_by_id", note_id=note_id))


    return await render_template("new_note.html")

@app.route("/notes/<note_id>", methods=["GET"])
@login_required
async def note_by_id(note_id: int):
    note_content = await db.get_note_content(user_id=g.user.user_id, note_id=int(note_id))
    return await render_template("note.html", note_id = note_id, content=note_content)

@app.route("/admin/users", methods=["GET"])
@login_required
@admin_required
async def users():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))


    total_users_count = await db.get_users_count()
    users_list = await db.get_users(limit=limit, offset=offset)

    return await render_template(
        "users.html",
        users=users_list,
        total_users_count=total_users_count,
        limit=limit,
        offset=offset
    )

@app.route("/admin/users/<username>/notes", methods=["GET"])
@login_required
@admin_required
async def users_notes(username: str):
    if not await db.is_user_exists(username):
        return redirect("/admin/users")

    notes_ids = await db.get_user_notes_by_username(username)

    return await render_template(
        "notes.html", notes_ids=notes_ids, is_admin=g.user.is_admin, username=username
    )

@app.route("/admin/users/<username>/notes/<note_id>", methods=["GET"])
@login_required
@admin_required
async def users_note_by_id(username: str, note_id: str):
    note_content = await db.get_user_note_content_by_username(username, int(note_id))

    return await render_template(
        "note.html", username=username, note_id=note_id, content=note_content, is_admin=g.user.is_admin
    )

@app.route("/go_away")
async def go_away():
    return await render_template("go_away.html")

@app.route("/logout", methods=["GET"])
@login_required
async def logout():
    resp = await make_response(redirect(url_for("index")))
    resp.delete_cookie('auth')
    return resp


if __name__ == "__main__":
    app.run()
