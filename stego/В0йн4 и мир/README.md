# В0йн4 и мир | medium | stego

## Информация
> Некоторые произведения лучше читать в оригинале...

## Выдать участникам
Текстовый файл [Task.txt](public/Task.txt) из директории [public/](public/)

## Описание
Участник используя информацию из файла, может найти оригинальную главу романа-эпопеи Толстова. Сравнив два этих документа можно найти различия в некоторых буквах и получить закодированный флаг.

## Решение
Прочитав описание таска и изучив текстовый файл, можно найти сайт, с которого был взят текст. Сравнив текст с сайта и данный в задание с помощью [программы](solve/solve.py) можно найти 17 несовпадающих букв: сеаХЕщдыещн_яршмЪ. Если переписать данную последовательность букв изменив раскладку клавиатуры на английский язык, то можно получить флаг.

## Hints
Как можно обнаружить изменения в файле? Возможно у тебя получится найти оригинал...

## Флаг
`ctf{Tolstoy_zhiv}`
