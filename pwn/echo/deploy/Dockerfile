FROM ubuntu:24.04

RUN apt-get -y update
RUN apt-get -y install socat

RUN useradd -m ctf
RUN mkdir /app
WORKDIR /app

COPY echo /app
COPY flag.txt /

USER ctf

EXPOSE 31313
CMD socat tcp-listen:31313,reuseaddr,fork exec:"./echo"
