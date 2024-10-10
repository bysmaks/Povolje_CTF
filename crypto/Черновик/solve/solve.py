def dehemming_it(r):
    n = [int(i) for i in r]
    p1 = n[0] + n[2] + n[4] + n[6] + n[8] + n[10]
    p2 = n[1] + n[2] + n[5] + n[6] + n[9] + n[10]
    p3 = n[3] + n[4] + n[5] + n[6] + n[11]
    p4 = n[7] + n[8] + n[9] + n[10] + n[11]
    p1 %= 2
    p2 %= 2
    p3 %= 2
    p4 %= 2
    num = int(str(p4) + str(p3) + str(p2) + str(p1), 2) - 1
    if num != -1:
        n[num] = int(not(bool(n[num])))
    s = ''
    for i in range(len(n)):
        if i not in [0, 1, 3, 7]:
            s += str(n[i])
    return int(s, 2)

with open("HemingWay.txt") as file:
    s = file.read().strip().split()
    for i in s:
        print(chr(dehemming_it(i)), end='')
