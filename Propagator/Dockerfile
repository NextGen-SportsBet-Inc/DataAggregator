# Propagator Dockerfile
FROM python:3.10-alpine

WORKDIR /app

COPY . /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]
