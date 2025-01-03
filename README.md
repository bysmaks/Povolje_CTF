# Povolje CTF (Code Camp Cup) - репозиторий для разработчиков

## Общая инфа

Дата проведения - 20 числа ноября.

Дедлайн по сдаче тасков - 6 ноября.

Формат флага `ctf{}` (регистронезависимый).

## По формату деплоя и репозитория

1. Все вещи, которые требуют развертывания на стороне сервера (web/ppc/etc) - деплояться **строго** через Dockerfile и docker-compose.yml. Пример можно найти [тут](example/sometask_1/deploy)
2. Каждый таск имеет описание по установленному шаблону, пример [тут](example/sometask_1/README.md)
3. Задания разбиты по категориям и заносятся в соответствующие директории.
4. Формат репозитория:
   - web (папка с названием категории)
     - task1 (папка с названием первого задания)
       - deploy (файлы необходимые для деплоя на сервер)
       - public (файлы, которые выдаются участникам, может быть пустой)
       - solve (файлы для решения задачи: подробное описание, эксплоиты, код)
       - src (файлы исходники, особенно для reverse / pwn категорий)
     - task2 (папка с названием второго задания)
       ...
     - task3 (папка с названием третьего задания)
       ...

## Как будем проводить тестирование

Тестирование задач проводится в три этапа:
1. Перекрестная оценка идеи задачи по таблице - если у вас возникает сомнение в адекватности того или иного таска - пишите в чат и тегайте автора и @by_sm
2. Тестирует сам автор, предоставляя полностью рабочий эксплоит
3. Перекрестное тестирование после деплоя на сервера.

## Если что-то пошло не так...

Не стесняемся, пишем в чат или в личку @by_sm

## UPDATE

Добавляем вкладку HINT / Подсказки:

Для easy - 0 подсказок
Для медиум - 1 подсказка
Для хард - 2 подсказки

