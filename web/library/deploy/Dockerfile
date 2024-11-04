FROM python:3.10-slim


WORKDIR /service
EXPOSE 8000

RUN apt update -y && \
	apt install -y --no-install-recommends wget xz-utils libfuse2 && \
    mkdir -p /vault/books && \
    mkdir -p /service/db && \
    touch /service/db/db.sqlite3 


RUN echo 'ctf{1_th1nk_1t_will_b3_e4sy!}' | base64 > /flag.txt
COPY requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY service /service

