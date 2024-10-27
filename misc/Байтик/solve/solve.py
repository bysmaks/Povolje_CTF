import os
res = b''

def find(path):
    if len(os.listdir('/'.join(path))) == 1:
        with open('/'.join(path) + '/part', 'rb') as file:
            s = file.read()
        if len(s) > 1:
            return 0
        global res
        res += s
        return 0
    for i in os.listdir('/'.join(path)):
        find(path + [i])
    return 0

find(['task'])
with open('res.png', 'wb') as file:
    file.write(res)
