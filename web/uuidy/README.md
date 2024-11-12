# uuidy | web | hard

## Информация

Заметки! Заметки! Заметки! Больше заметок богу заметок!

Флаг `ctf{<password_hash>}`, где <password_hash> - хеш пароля админа.

## Деплой

Перед деплоем нужно настроить некоторые енвы в [deploy/docker/docker-compose.yaml](deploy/docker/docker-compose.yaml).
- Выставите валидный токен телеграм бота в переменной `TG_BOT_TOKEN`.  
- В `SERVICE_HOST` впишите адрес сервера и порт на котором деплоите сервис, например `185.74.123.12:7777` (7777 - порт из компоуза).

Деплой сервиса
```sh
cd deploy/docker
docker compose -f docker-compose.yaml up -d
```

После деплоя сервиса, хеш пароля админа (для флага), можем достать командой:
```
docker compose exec uuidy_postgres psql -U postgres -d postgres -c "SELECT username, password_hash FROM users WHERE username='admin';"
```

## Выдать участникам

Скинуть архив: [public/uuidy.tar.gz](public/uuidy.tar.gz).

## Хинты

HINT #1:  
- Лкально: [hint1.jpg](hints/hint1.jpg)
- На imgBB: https://ibb.co/z6jGj9L

HINT #2:
- Локально: [hint2.jpg](hints/hint2.jpg)
- На imgBB: https://ibb.co/Xb1qDTQ

## Решение

В сервисе есть возможность авторизации через Telegram, ссылки для входа генерятся time based функцией `secure_uuid`, т.е.
`зная 2 ссылки мы можем сгенерить ссылки, которые были между ними`.  

Делаем запрос на вход через Telegram в **свой аккаунт**, потом в **аккаунт admin**, потом снова в **свой аккаунт**.
`(по коду видно, что даже если сервис выводит 'У юзера не настроен вход через Telegram!' токен всё равно генерится и сохраняется)`.
Берем 2 ссылки на вход в наш аккаунт и генерим все ссылки между. Для каждой ссылки делаем запрос и ищем ту, что установит нам auth куки для admin аккаунта.  
Пример скрипта в [solve/crack_signin_link.py](solve/crack_signin_link.py).  

В админке есть blind sql в ручке `/admin/users/<username>/notes`, в вызове функции `is_user_exists` запрос 
`result = await con.fetch(f"SELECT EXISTS ( SELECT user_id FROM users WHERE username = '{username}' )")`.
На место username можем инъектить что-то типа `admin' AND password_hash LIKE '{password_hash_substr}%`, 
если подстрока `password_hash_substr` совпадёт, то запрос вернёт `200`, иначе будет `302` (редирект), таким образом брутим хеш пароля
от аккаунта **admin**.   
Пример скрипта в [solve/brute_password_hash.py](solve/brute_password_hash.py)

Итоговое решение:
1. Регистрируем любой аккаунт, настроиваем в нём вход через Telegram;
2. Генерим ссылку на вход через Telegram на свой аккаунт, потом на аккаунт админа, потом снова на свой;
3. Брутим ссылку на вход в аккаунт админа;
4. Брутим хеш пароля админа через blind sql в ручке `/admin/users/<username>/notes`
5. Оборачиваем хеш в `ctf{}`, флаг готов

## Флаг

`ctf{178b3c72fb24a69e1e3d8a983f35eb8f1dc4abe55d0ff69c7a7a1a3b933989aa}`

Для проверки, что хэш пароля админа не изменился, можно достать его командой:
```sh
cd deploy/docker
docker compose exec uuidy_postgres psql -U postgres -d postgres -c "SELECT username, password_hash FROM users WHERE username='admin';"
```