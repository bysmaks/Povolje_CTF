import random
import string
from RegexGenerator import RegexGenerator
from art import text2art
from re import match
from os import getenv
from termcolor import colored
from time import sleep

flag = getenv("FLAG", "ctf{sup3r_asc11_@rt!}")

def generate_random_sequence(length):
    all_possible_chars = string.ascii_letters + string.digits + string.punctuation
    all_possible_chars = all_possible_chars.replace("'", "")\
                                           .replace("\\", "")\
                                           .replace("/", "")\
                                           .replace("^", "")\
                                           .replace("%", "")\
                                           .replace("$", "")\
                                           .replace("@", "") #некоторые спецсимволы могут жестко покараптить перевод regex'a в ascii
    random_sequence = ''.join(random.choice(all_possible_chars) for _ in range(length))
    return random_sequence

def regex_generator(sequence):
    return RegexGenerator(sequence).get_regex()

def ascii_art(regex):
    ascii_art_parts = [text2art(char) for char in regex]
    ascii_art_string = "\n".join(ascii_art_parts)
    print(ascii_art_string)

print(colored("Попытка входа в храм адептов Механикуса, необходима дополнительная проверка...", "blue", "on_white"))
sleep(1)
print(colored("Сканирование на наличие живых организмов запущено...", "blue", "on_white"))
sleep(1)
print(colored("Ошибка сканирования!", "red", "on_white"))
sleep(1)
print(colored("Подозрение на не механическую форму жизни, требуется проверка!", "red", "on_white"))
sleep(1)

count = 0
while True:    
    sequence = generate_random_sequence(random.randint(3,7))
    regex = regex_generator(sequence)
    
    if not match(regex, sequence): # проверка что это выражение вообще работает (могут быть коррапты при генерации)
        continue
    #print(f"Sequence: {sequence}") #debug mode
    #print(f"Regex: {regex}") #debug mode
    
    ascii_art(regex)
    
    answer = input(colored("Введите последовательность, соответствующую данному регулярному выражению: ", "green"))

    if match(regex, answer):
        count += 1
        print(colored(f"Count: {count}/150\n", "green"))

    else:
        print(colored("Обнаружена попытка проникновения человеком, режим уничтожения активирован!", 'red', 'on_yellow'))
        exit(0)

    if count == 150:
        print(colored(f"Добро пожаловать адепт Механикус! Лови свой флаг:\n {flag}", "blue", "on_white"))
        exit(0)