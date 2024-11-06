#!/bin/bash

echo -n "[STEP 1] Enter the ip/domen for openvpn in format - 'udp://domen.com': "
read domen_openvpn
bash -c "docker compose run --rm openvpn ovpn_genconfig -u $domen_openvpn"
echo -n "[STEP 1] At the next steps of program type password with length more then 4. On the other question you make press only Enter"
read
bash -c "docker compose run --rm openvpn ovpn_initpki"
mv config/openvpn.conf config/openvpn.conf.bak
sed -e '/persist-tun/a \
duplicate-cn' \
-e '/route 192.168.254.0 255.255.255.0/a \
route 10.0.0.0 255.255.0.0' \
-e '/push "comp-lzo no"/a \
push "route 10.0.0.0 255.255.0.0"' \
config/openvpn.conf.bak > config/openvpn.conf
bash -c "docker compose run --rm openvpn easyrsa build-client-full test nopass"
bash -c "docker compose run --rm openvpn ovpn_getclient test > certificate.ovpn"
bash -c "openssl req -new -x509 -key asterisk-config/keys/asterisk.key -out asterisk-config/keys/asterisk.crt -days 365"
python3 changer.py
if [ $? -eq 0 ]
then
  bash -c "docker compose up -d"
fi

