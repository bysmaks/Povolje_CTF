a =[['c'], ['t'], ['f'], ['{'], ['a', 'c', 'e', 'g', '_'], ['e', 'g', 'i', 'k', 'u', 'w', 'y', '5', '7', '9', '{'], ['p'], ['h'], ['c', 'e', 'k', 'm', 's', 'u', '}', '{'], ['r'], ['_'], ['i'], ['s'], ['a', 'c', 'e', 'g', '_'], ['u', 'w', 'y', '{'], ['c', 'e'], ['a', '_'], ['k'], ['a', '_'], ['f', 'j', 'v', 'z', '6'], ['c', 'e'], ['r'], ['y'], ['_'], ['k', 'm', 's', 'u'], ['a'], ['d'], ['}']] 
s = 1
for el in a:
    s *= len(el)
print(s)
from itertools import product
combinations = list(product(*a))
t = []
print(len(combinations))
for combination in combinations:
    tmp = ''.join(combination)
    t.append(tmp)
#print(t)
data = []
words = set(open("words.txt", 'r').read().split("\n"))
for el in t:
    words_flag = el[4:-1].split("_")
    #print(words_flag)
    c = 0
    for word_flag in words_flag:
        if word_flag in words:
            c += 1
    if c > 3:
        print(el)
        data.append(el)
print('no' in words)
f = open('test.txt', 'w')
f.write("\n".join(t))
f.close()

f = open('flags.txt', 'w')
f.write("\n".join(data))
f.close()

print(s)
#print(len(t))
# k = 39
# for i in range(32, 127):
#     for j in range(32, 127):
#         if i != j and (k-i)^(k+i) == (k-j)^(k+j):
#             print(i, j)


# (k-i)^(k+i) -> a^(a+2b) 00