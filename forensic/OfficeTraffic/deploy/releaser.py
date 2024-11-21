from scapy.all import *

print("Next process may be long, about 2 minutes!")
cert_old = open("old-config/certificate.ovpn", "rb").read()
cert_new = open("certificate.ovpn", "rb").read()

#print(len(tuple(filter(lambda x: not x, cert_new.split(b"\n")))))

cert_new = cert_new.replace(b"\n\n", b"\n", len(cert_new) - len(cert_old))

packets = sniff(offline="release.pcapng")

##print(len(cert_old), len(cert_new))
fp = packets[75948]
sp = packets[75951]
fp.load = fp.load.replace(cert_old[:4080], cert_new[:4080])
sp.load = sp.load.replace(cert_old[4080:], cert_new[4080:])
wrpcap("../public/release.pcapng", packets)
