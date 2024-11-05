FROM python:3.9-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["hypercorn", "app:app", "-w", "1", "-b", "0.0.0.0:5000", "--access-log", "-"]
