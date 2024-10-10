with open("Original.txt", 'r', encoding='utf-8') as file:
    orig = ''.join(file.read().strip().split())

with open("В0йн4 и мир.txt", 'r', encoding='utf-8') as file:
    task = ''.join(file.read().strip().split())

for i in range(len(orig)):
    if orig[i] != task[i]:
        print(task[i], end='')

