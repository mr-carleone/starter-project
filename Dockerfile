FROM python:3.13-slim

ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-traditional

COPY requirements /app/requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/dev.txt

COPY . .

EXPOSE 8000
