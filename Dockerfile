FROM python:3.13-slim

ENV PYTHONPATH=/app

WORKDIR /app

# Установка системных зависимостей (выполняется от root)
RUN apt-get update && \
    apt-get install --no-install-recommends -y netcat-traditional && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей и установка (выполняется от root)
COPY requirements /app/requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/dev.txt

COPY . .

EXPOSE 8000
