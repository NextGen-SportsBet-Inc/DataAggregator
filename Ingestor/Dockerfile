# Ingestor Dockerfile
FROM python:3.12-alpine

WORKDIR /app/Ingestor

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/Ingestor

CMD ["python", "src/main.py"]
