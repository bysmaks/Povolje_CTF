# stack_cryptor | medium | reverse

## Информация

> stack_cryptor
> Нашёл простой шифровальщик, бинарник есть, но архитектура какая-то странная...
>
> ./vm program.bin

## Выдать участинкам
Архив из директории [public/](public/)

## Описание
Необходимо понять архитектуру виртуальной машины, какие опкоды и операнды соотносятся каким байтам. Далее необходимо разборать бинарник, понять алгоритм "шифрования". Затем его обратить и восстановить флаг.
*Дебаг символы специально оставлены для упрощения решения.*

## Решение
Сам алгоритм [на C](solve/solution.c) [на асме](solve/program.s)

## Флаг

`ctf{vms_3re_qu1t3_funny_3a4gb9}`

