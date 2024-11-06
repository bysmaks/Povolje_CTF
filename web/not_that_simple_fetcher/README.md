# not_that_simple_fetcher | simple | web

## Информация

> В прошлый раз, мой просматриватель сайтов поломали хакеры :( \
> Я переписал его, и сейчас он полностью безопасен!
> http://\<ip>:5464
> 

## Deploy

```sh
cd deploy
docker compose up --build -d
```

## Выдать участникам

IP:PORT

## Хинты

\-

## Решение

Делаем обычный redirect to localhost через сторонний ресурс, обходя внутреннюю проверку на обращение к localhost.

[Пример сервера](solve/server.py)

Примеры открытых редиректоров на localhost:

localtest.me
localh.st
company.127.0.0.1.nip.io

Отправляем сервер по http://<attacker_public_ip>:5000/ и получаем флаг.

## Флаг

`ctf{w0w_n0w_y0u_kn0w_wh47_r3d1r3c7_70_l0c4lh057_15}`