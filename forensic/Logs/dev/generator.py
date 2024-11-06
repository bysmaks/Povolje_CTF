# cat log.txt | grep flag | python3 -c "import sys;print(''.join([i.split('flag.php/')[1].split()[0] for i in sys.stdin]))"
import random
import datetime
import logging

# Настройка логирования
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Список возможных типов сообщений
message_types = ['INFO', 'WARNING', 'ERROR']

# Список возможных действий
actions = ['GET', 'POST', 'PUT', 'DELETE']

# Список возможных URL
urls = ['/index.html', '/login.php', '/admin/dashboard', '/api/data']

# Список возможных IP-адресов
ips = ['192.168.1.100', '10.0.0.1', '172.16.254.1', '8.8.8.8']

# Список возможных пользователей
users = ['admin', 'user1', 'user2', 'guest']

# Список возможных агентов
agents = ['Mozilla/5.0', 'Google Chrome', 'Firefox/75.0', 'Safari/537.36']

# Флаг
flag = "ctf{4n4lyz1n6_7h3_w3b_l06}"
c = 0
# Генерация лог-файла
for i in range(random.randint(10, 37)):
    message_type = random.choice(message_types)
    action = random.choice(actions)
    url = random.choice(urls)
    ip = random.choice(ips)
    user = random.choice(users)
    agent = random.choice(agents)

    # Генерация сообщения
    if message_type == 'INFO':
        message = f'{action} {url} от {ip} ({user}) с агентом {agent}'
        logging.log(logging.INFO, message)
    elif message_type == 'WARNING':
        message = f'{["Неудачная", "Удачная"][random.randint(0, 1)]} попытка авторизации от {ip} ({user})'
        logging.log(logging.WARNING, message)
    elif message_type == 'ERROR':
        message = f'Ошибка при обработке запроса {action} {url} от {ip} ({user})'
        logging.log(logging.ERROR, message)

while c < len(flag):
    message_type = random.choice(message_types)
    action = random.choice(actions)
    url = random.choice(urls)
    ip = random.choice(ips)
    user = random.choice(users)
    agent = random.choice(agents)

    # Генерация сообщения
    if message_type == 'INFO':
        if action == "PUT":
            message = f'{action} /flag.php/{flag[c]} от {ip} ({user}) с агентом {agent}'
            c += 1
        else:
            message = f'{action} {url} от {ip} ({user}) с агентом {agent}'
        logging.log(logging.INFO, message)
    elif message_type == 'WARNING':
        message = f'{["Неудачная", "Удачная"][random.randint(0, 1)]} попытка авторизации от {ip} ({user})'
        logging.log(logging.WARNING, message)
    elif message_type == 'ERROR':
        message = f'Ошибка при обработке запроса {action} {url} от {ip} ({user})'
        logging.log(logging.ERROR, message)
for i in range(random.randint(10, 37)):
    message_type = random.choice(message_types)
    action = random.choice(actions)
    url = random.choice(urls)
    ip = random.choice(ips)
    user = random.choice(users)
    agent = random.choice(agents)

    # Генерация сообщения
    if message_type == 'INFO':
        message = f'{action} {url} от {ip} ({user}) с агентом {agent}'
        logging.log(logging.INFO, message)
    elif message_type == 'WARNING':
        message = f'{["Неудачная", "Удачная"][random.randint(0, 1)]} попытка авторизации от {ip} ({user})'
        logging.log(logging.WARNING, message)
    elif message_type == 'ERROR':
        message = f'Ошибка при обработке запроса {action} {url} от {ip} ({user})'
        logging.log(logging.ERROR, message)
