# ezshell | HARD | PWN

## Информация

> Zdarova, osilish takuyu zadachku?
>
> nc ip:15557

## Деплой

```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Файл из директории [public/](public/) и IP:PORT сервера

## Описание

Shellcode using many chunks lenght of 6 bytes

## Решение

[Эксплоит](solve/sploit.py)

## Hints

1) Put jump at the end of chunks

2) Executable memory is rwx

## Флаг

`ctf{nelineyniy_shellcod_bil_ne_tak_uzh_i_slozhen???}`
