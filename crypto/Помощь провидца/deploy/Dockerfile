FROM python:3

COPY ./app /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -w 10 -k uvicorn.workers.UvicornWorker server:app -b 0.0.0.0:8080
