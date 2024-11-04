FROM ubuntu:24.04

RUN apt-get -y update
RUN apt-get -y install socat

RUN useradd -m ctf
RUN mkdir /app
WORKDIR /app

COPY chall /app
COPY flag.txt /

USER ctf

EXPOSE 37373
CMD socat tcp-listen:37373,reuseaddr,fork exec:"./chall"
