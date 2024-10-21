import random
import string
import datetime

from tqdm import tqdm
from itertools import product

# считаем количество секунд, которое прошло с начало года до дня реализации шифра
first_date = datetime.datetime(1970, 1, 1)
time_since = int((datetime.datetime(2024, 10, 17) - first_date).total_seconds())


# функция расширофки
def decrypt(key, enc):
    # функция возвращет массив из массивов, где в каждом субмассиве варинты 
    decs = []
    for i in range(len(enc)):
        tmp = []
        if enc[i] - key[i] >= 32 and enc[i] - key[i] <= 126:
            if enc[i] - key[i] >= key[i]:
                tmp.append(chr(enc[i] - key[i]))
        if enc[i] % 2 == 0: # если нечетный, то точно сумма
            for j in (string.ascii_lowercase + "_}{"):
                if (ord(j) + key[i]) ^ (key[i] - ord(j)) == enc[i]:
                    if key[i] > ord(j): # проверяем попали мы бы в xor, когда шифровали открытый текст
                        tmp.append(j)
        decs.append(tmp)
    return decs

#начинаем перебор сидов для рандома
for i in tqdm(range(time_since, time_since+3600*24)):
    random.seed(i)
    flag = [218, 224, 182, 203, 334, 246, 352, 172, 314, 134, 179, 168, 161, 462, 278, 202, 194, 160, 322, 244, 458, 138, 232, 125, 362, 138, 115, 382]
    key = bytearray(random.getrandbits(8) for _ in range(len(flag)))
    data = decrypt(key, flag)

    flag_print = all([len(i) for i in data]) # проверяем, что у нас есть символы на каждом месте
    if flag_print:
        # знаем точный формат флага, поэтому он всегда будет начинаться с `ctf{`  и заканчиватся `}`
        data[0] = ['c'] 
        data[1] = ['t']
        data[2] = ['f']
        data[3] = ["{"]
        data[-1] = ["}"]

        combinations = product(*data)

        words = set(open("wordlist.txt", 'r').read().split("\n")) # подгружаем словарь английского языка

        for combination in combinations:
            tmp = ''.join(combination)
            words_flag = tmp[4:-1].split("_") # убираем `ctf{` и `}`
            c = 0 # счетчки распознанных слов в флаге

            for word_flag in words_flag:
                if word_flag in words:
                    c += 1

            if c > 4:
                print(tmp)
