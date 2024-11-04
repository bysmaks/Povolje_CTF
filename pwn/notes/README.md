# notes | EASY | PWN

## Информация

> Привет, еще одно задание на записки?
>
> nc ip:37373

## Деплой

```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Файл из директории [public/](public/) и IP:PORT сервера

## Описание

Суть переписать функцию структуры на свою через переполнение.

## Решение

[Эксплоит](solve/exploit.py)

## Флаг

`ctf{dont_save_functions_inside_structs_pls_okay}`
