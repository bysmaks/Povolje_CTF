# echo | EASY | PWN

## Информация

> Чем дольше ты смотришь в бездну, тем больше бездна смотрит на тебя...
>
> nc ip:31313

## Деплой

```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Архив из директории [public/](public/) и IP:PORT сервера

## Описание

Суть сделать обычную формат стрингу и вызвать one_gadget

## Решение

[Эксплоит](solve/exploit.py)

## Флаг

`ctf{i_hate_format_string_do_you_too_hm}`
