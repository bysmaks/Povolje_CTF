FROM python:3.10-alpine

ADD ./app /app

WORKDIR /app

RUN apk add --no-cache socat
RUN chmod +x /app/run.sh /app/main.py
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "sh", "run.sh" ]
