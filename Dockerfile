FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements /app/requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/dev.txt

COPY . .

EXPOSE 8000
