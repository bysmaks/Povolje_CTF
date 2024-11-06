import sys
data1 = open("release.pcapng", "rb").read()
cert_old = open("old-config/certificate.ovpn", "rb").read().split(b'\n')
cert_new = open("certificate.ovpn", "rb").read().split(b'\n')
##print(len(cert_old), len(cert_new))
sp = []
with open("../public/release.pcapng", "wb") as f:
    m = -1
    for k, i in enumerate(data1.split(b"\n")):
        if m >= k:
            continue
        if i in cert_old and i:
            if cert_old.index(i) in sp:
                index = cert_old.index(i, cert_old.index(i) + 1)
            else:
                index = cert_old.index(i)
            f.write(cert_new[index] + b'\n')
##            print(index + 1, i, ">", cert_new[index])
            sp.append(index)
        elif i.startswith(b"EfMeTX0ZqRo7zBhKpeCwlAfh"):
            payload = b""
##            print(k)
            payload = i.replace(b"EfMeTX0ZqRo7zBhKpeCwlAfhC7vOOMnJVEHMtFzbjILHcarxWlShp", cert_new[cert_old.index(b"EfMeTX0ZqRo7zBhKpeCwlAfhC7vOOMnJVEHMtFzbjILHcarxWlShpjTTcwMOyGut")][:53])
##            print(cert_old.index(b"EfMeTX0ZqRo7zBhKpeCwlAfhC7vOOMnJVEHMtFzbjILHcarxWlShpjTTcwMOyGut") + 1, i, '>', payload)
            f.write(payload + b'\n')
            m = k
            for j in data1.split(b"\n")[k + 1:]:
                m += 1
                if b'jTTcwMOyGut' in j:
                    payload = j.replace(b'jTTcwMOyGut', cert_new[cert_old.index(b"EfMeTX0ZqRo7zBhKpeCwlAfhC7vOOMnJVEHMtFzbjILHcarxWlShpjTTcwMOyGut")][53:])
##                    print(cert_old.index(b"EfMeTX0ZqRo7zBhKpeCwlAfhC7vOOMnJVEHMtFzbjILHcarxWlShpjTTcwMOyGut") + 1, j, '>', payload)
                    f.write(payload + b'\n')
                    break
                else:
                    f.write(j + b'\n')
            sp.append(cert_old.index(b"EfMeTX0ZqRo7zBhKpeCwlAfhC7vOOMnJVEHMtFzbjILHcarxWlShpjTTcwMOyGut"))
        else:
            f.write(i + b'\n')
if len(list(filter(lambda x: cert_old.index(x) not in sp and x, cert_old))) == 0 and len(list(filter(lambda x: cert_new.index(x) not in sp and x, cert_new))) == 0:
    print("\033[0;32mSuccess!\033[0m")
else:
    print("\033[0;31mError, Restart deploy!!!\033[0m")#, list(filter(lambda x: cert_old.index(x) not in sp, cert_old)), list(filter(lambda x: cert_new.index(x) not in sp, cert_new)))
    sys.exit(1)
