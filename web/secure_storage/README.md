# secure_storage | medium | web 

## Информация

> To store, or not to store, that is the question
> 
> http://<ip>:9999

## Деплой

Деплой сервиса
```sh
cd docker
docker compose -f docker-compose-prod.yaml -p secure_storage up -d
```

Сервис поднимется на 9999 порту. Флаг и место его хранения можно менять в Dockerfile.

## Выдать участникам

Скинуть архив: [public/secure_storage_public.tar.gz](public/secure_storage_public.tar.gz).

IP:PORT

## Хинты

HINT #1:  
- Локально: [hint1.png](hints/hint1.png)
- На imgBB: https://ibb.co/ZKNsSMv

## Решение

Регистрация в сервисе происходит через отправку формы с полем `data` в которое вписан JSON вида:
```json
{"username":  "user", "password": "password"}
```
Эту JSON'ку сервис напрямую сериализует в GO'шную структуру `User` и потом пытается сохранить в БД, не зануляя остальные поля.
У `User` есть поле `IsPaid`, которой соответствует JSON поле `is_paid`, если мы это поле пропишем в отправляемом JSON, типа:
```json
{"username":  "user", "password": "password", "is_paid":  true}
```
В итоге сервис запишет нас в БД как платного юзера.

У платных юзеров есть доступ к функционалу с папками, уязвимому к PathTraversal. Можем отправить запрос типа:
```GET /folder/../..```
Чтобы ходить по другим директориям сервиса и смотреть что там за файлы. Увидим что на два уровня выше лежит файл `flag.txt`.

Можем выгрузить его с помощью запроса:
```GET /file/flag.txt/folder/../..```

Итоговое решение:
1. Регистрируем аккаунт платного юзера через кривую сериализацю JSON;
2. Эксплойтим Path Traversal, находим флаг на две директории выше, выгружаем его;

## Флаг

`ctf{to_marsh4l_or_not_t0_mar5hal_tha7_1s_the_path_trav3rsal}`
