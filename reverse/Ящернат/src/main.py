import hashlib

def st1(password):
    ind = [36, 34, 15, 3, 29, 7, 26, 21, 27, 17, 30, 32, 19, 23, 25, 31, 1, 14, 33, 20, 12, 37, 10, 24, 6, 18, 13, 16, 9, 0, 11, 35, 4, 8, 22, 28, 2, 5]
    return [ord(password[i]) for i in ind]


def st2(password):
    nums = [0x33, 0x61, 0x3e, 0x4e, 0x26, 0xa, 0x33, 0x57, 0x5c, 0x1a, 0xf, 0x24, 0x61, 0x4b, 0x46, 0x64, 0x59, 0x1e, 0x19, 0x1c, 0x1f, 0x34, 0xd, 0x16, 0x41, 0x2d, 0x48, 0x3a, 0x4c, 0x52, 0x40, 0x58, 0x4c, 0x37, 0x3a, 0x3c, 0xb, 0x60]
    return [password[i] ^ nums[i] for i in range(len(nums))]


def st3(password):
    s = "".join(list(map(chr, password)))
    current = []
    for i in s:
        md5_hash = hashlib.md5(i.encode())
        md5_hex = md5_hash.hexdigest()
        current.append(md5_hex)
    return current
    


def main():
    correct = ['518ed29525738cebdac49c49e60ea9d3', '15f41a2e96bae341dde485bb0e78f485', '815417267f76f6f460a4a61f9db75fdb', '336d5ebc5436534e61d16e63ddfca327', '0cc175b9c0f1b6a831c399e269772661', '92eb5ffee6ae2fec3ad71c777531578f', '2db95e8e1a9267b7a1188556b2013b33', 'c4ca4238a0b923820dcc509a6f75849b', '8bb6c17838643f9691cc6a4de6c51709', '3a3ea00cfc35332cedf6e5e9a32e94da', '8d9c307cb7f3c4a32822a51922d1ceaa', 'dfcf28d0734569a6a693bc8194de62bf', '47ed733b8d10be225eceba344d533586', '45c48cce2e2d7fbdea1afc51c7c6ad26', '3590cb8af0bbb9e78c343b52b93773c9', '9eecb7db59d16c80417c72d1e1f4fbf1', '7215ee9c7d9dc229d2921a40e899ec5f', '83878c91171338902e0fe0fb97a8c47a', '9371d7a2e3ae86a00aab4771e39d255d', '0d61f8370cad1d412f80b84d143e1257', '5058f1af8388633f609cadb75a75dc9d', '89e74e640b8c46257a29de0616794d5d', 'e1e1d3d40573127e9ee0480caf1283d6', 'dd7536794b63bf90eccfd37f9b147d7f', '7bc72a0767d237be4da30ace191acdc2', '02129bb861061d1a052c592e2dc6b383', '6666cd76f96956469e7be39d750cc7d9', '7e6a2afe551e067a75fafacf47a6d981', 'd1457b72c3fb323a2671125aef3eab5d', 'ad1e41cebd43e64af1a28d4d70dc9e30', 'eccbc87e4b5ce2fe28308fd9f2a7baf3', '3389dae361af79b04c9c8e7057f60cc6', '336d5ebc5436534e61d16e63ddfca327', '5206560a306a2e085a437fd258eb57ce', '68b329da9893e34099c7d8ad5cb9c940', '58c89562f58fd276f592420068db8c09', 'b9ece18c950afbfa6b0fdbfa4ff731d3', '15f41a2e96bae341dde485bb0e78f485']
    password = input("Причина пропуска? ")
    if len(password) != 38:
        print("Принича не уважительная. Вы отчислены!")
        return
    stage1 = st1(password)
    stage2 = st2(stage1)
    stage3 = st3(stage2)
    if correct == stage3:
        print("Причина уважительная! Мы не отчислим вас!")
    else:
        print("Принича не уважительная. Вы отчислены!")


if __name__ == "__main__":
    main()