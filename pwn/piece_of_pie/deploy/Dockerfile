FROM ubuntu:24.10

RUN apt-get -y update
RUN apt-get -y install socat

RUN useradd -m ctf
RUN mkdir /app
WORKDIR /app

# COPY ld-linux-x86-64.so.2 /
# COPY libc.so.6 /
COPY piece_of_pie /app
COPY flag /app

USER ctf

EXPOSE 17171
CMD socat tcp-listen:17171,reuseaddr,fork exec:"./piece_of_pie"
