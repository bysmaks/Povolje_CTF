# Ded | hard | reverse

## Информация

> Текст, который будет приложен к заданию
> Can you beat this ded?

## Выдать участинкам

Архив из директории [public/](public/)

## Описание

ROP-based vm. 

## Решение

Rop-based виртуалка. Дебажим и смотрим, что в результате ропа просто происходит xor входного буфера с константными чиселками. Дексорим константную строку с чиселками и получаем флаг.

## Hints

1) Return oriented programming

2) Xor cipher

## Флаг

`ctf{rop_based_vm_is_ezzzzzzz}`

