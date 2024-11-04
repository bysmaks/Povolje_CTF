# mother
ind = list(map(int, "6,1,9,10,8,4,7,5,3,11,2".split(",")))
s = list(map(int, "48,99,48,117,121,123,95,100,102,95,116".split(",")))

res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(len(ind)):
    res[ind[i] - 1] = chr(s[i])

print("".join(res), end="")

#father
s2 = "1011000, 0000101, 1011111, 1010001, 1101011, 1110010, 1110101, 1111101, 1100110, 1101101, 1100000, 1110101, 1111000, 1110001, 1100111, 1101011"
s2 = s2.split(", ")
for i in s2:
    print(chr(int(i, 2) ^ 52), end="")

#grandmother
s3 = list(map(int, "109,110,118,62,124".split(",")))
for i in s3:
    print(chr(i + 1), end="")

print()