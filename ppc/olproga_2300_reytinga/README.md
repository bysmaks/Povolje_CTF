# olproga_2300_reytinga | medium | ppc

### Информация
> Дроби всякие нужны,
> Дроби всякие важны.
> Дробь учи, тогда сверкнет тебе удача.
> Если будешь дроби знать,
> Точно смысл их понимать,
> Станет легкой даже трудная задача.
> `nc host 11337`

### Деплой
```shell
cd deploy
docker-compose up --build
```

### Выдать участникам
Файл из папки [public](public) и `host:port` сервера

### Описание
Гуглим и пишем нужную программу на fractran

### Решение

Немного погуглив языки программирования с дробями можно наткнуться на [fractran](https://ru.wikipedia.org/wiki/FRACTRAN) и, например, адаптировать программу умножения оттуда, либо придумать ее самому :)

#### Пример возможного решения:

> $\Large\frac{5\ast7}{2};\frac{3\ast11\ast13}{17};\frac{17}{7\ast11};\frac{1}{11};\frac{7}{13};\frac{11}{5};\frac{1}{7}$ 

##### Решение реализовано с помощь алгоритма умножения, поскольку нужно вывести число 3 в степени $\Large n^n$ 
##### Проанализируем принцип работы программы

1. Дробь $\Large\frac{5\ast7}{2}$ создет цикл, который при каждой итерации вычитает 1 из степени
   простого числа 2 и добавляет 1 числам 5 и 7. Можно представить это в виде:
   ```python
   while var_2 > 0: # var_n - степень простого числа n
     var_2 -= 1
     var_5 += 1
     var_7 += 1 
    ```
   Для простоты обозначим степень числа 5 за `a`, степень числа 7 за `b`. Теперь необходимо
   передать простому числу 3 степень `a*b` 
2. Дробь $\Large\frac{11}{5}$ заменяет один множитель 5 на множитель 11. Число 11 является
   флагом, что программа вычла из степени числа 5 единицу (`a-1`), но еще не прибавили степень
   числа 7 к результату. 
3. Дробь $\Large\frac{7}{11}$ инициализиурет процесс добавления  к результату. Мы убираем
   множитель 7 и множитель 11 (флаг, описанный в п.2) и создаём новый флаг 17 (`var_17`) , который
   означает, что программа вычла `b-1`, но не закончила складывать с итоговым результатом
   степени числа 3.
4. Дробь $\Large\frac{3\ast11\ast13}{17}$ указывает на то, что если убрали семерку, то можем
   прибавить единицу к показателю степени три. А также нужно добавить флаги для продолжения
   сложения, так как прибавили только единицу к результату, но нам нужно прибавить `b`. Пункт 3
   и 4 по сути цикл прибавления b к степени тройки
5. Дробь $\Large\frac{7}{13}$ говорит о том, что если пункты 2 и 3 не сработали (то есть `b=0`
   ), то мы закончили прибавление, и нужно вернуть ему исходное значение. Поскольку в пункте 4
   при каждой итерации `b-1` добавляли `var_13+1`, то теперь можем восстановить с помощью
   данной дроби.
6. Наконец, после когда  `a и b` обнулятся, то дробь $\Large\frac{1}{7}$, очистит оставшийся флаг `var_7`

> Удобный step-by-step [онлайн-интерпретатор](https://tjwei.github.io/Fractran/)

### Флаг
`ctf{1_f3ll_1n_l0v3_w1th_y0u_1n_frAct10n5}`

### Подсказка
> oeis A007542
