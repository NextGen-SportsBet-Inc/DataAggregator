# Wrappers Dockerfile
FROM python:3.12-alpine

WORKDIR /app/Wrappers

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/Wrappers

CMD ["python", "src/main.py"]
