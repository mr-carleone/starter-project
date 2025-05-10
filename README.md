# 🚀 Starter Project

![FastAPI](https://img.shields.io/badge/FastAPI-0.109.1-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0.7-2496ED?logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.28-FF4500)
![Pydantic](https://img.shields.io/badge/Pydantic-2.5.3-%2300C7B7)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.25.0-499848)

## Шаблон для быстрого старта проектов на FastAPI с поддержкой:

- 🐳 Docker-контейнеризации
- 🐘 Подключения к PostgreSQL
- 📊 Автоматической документацией Swagger/Redoc
- 🛠️ Настроенным логированием (цветным для разработки)
- 🔄 Миграциями через Alembic

## 🌟 Особенности

- ✅ Готовый к продакшену стартер
- ✅ Раздельные настройки для dev/prod
- ✅ Репозиторий-паттерн для работы с БД
- ✅ Валидация через Pydantic v2
- ✅ Автоматическое создание миграций
- ✅ Тестовые данные при инициализации

## 🚦 Быстрый старт

### Предварительные требования

- Docker 24.0+
- Docker Compose 2.20+

```bash
# Клонировать репозиторий
$ git clone https://github.com/mr-carleone/starter-project.git
$ cd starter-project

$ cp .env.template .env

$ docker network create app-net

# запустить по очереди сервисы
# зависимости если нужно postgres, pgadmin
$ docker-compose -f docker-compose.deps.yml up -d
# основное приложение
$ docker-compose -f docker-compose.yml up -d

# Создать первоначального пользователя
# 1 INITIAL_USER_TOKEN=8c6256c0-9db7-4e0d-ba61-1dee5eea40aa  заменить на свой
# 2 /api/v1/init/ выполнит инициализацию предварительно добавив свой api-key в header
```

API будет доступно по адресу:
http://localhost:8000

## 📚 Документация

После запуска проекта будет доступна:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- Healthcheck: [http://localhost:8000/healthcheck](http://localhost:8000/healthcheck)

## 🛠 Технологии

<table>
    <thead>
        <tr>
            <th>Технология</th>
            <th>Версия</th>
            <th>Назначение</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>FastAPI</td>
            <td>0.109.1</td>
            <td>Основной фреймворк API</td>
        </tr>
        <tr>
            <td>Python</td>
            <td>3.11</td>
            <td>Базовый язык</td>
        </tr>
        <tr>
            <td>PostgreSQL</td>
            <td>16</td>
            <td>Основная база данных</td>
        </tr>
        <tr>
            <td>SQLAlchemy</td>
            <td>2.0.28</td>
            <td>ORM для работы с БД</td>
        </tr>
        <tr>
            <td>Alembic</td>
            <td>1.13.1</td>
            <td>Управление миграциями</td>
        </tr>
        <tr>
            <td>Pydantic</td>
            <td>2.5.3</td>
            <td>Валидация данных</td>
        </tr>
        <tr>
            <td>Uvicorn</td>
            <td>0.25.0</td>
            <td>ASGI-сервер</td>
        </tr>
        <tr>
            <td>Docker</td>
            <td>24.0.7</td>
            <td>Контейнеризация приложения</td>
        </tr>
    </tbody>
</table>

## 📂 Структура проекта

```
fastapi-starter/
├── src/
│   ├── core/          # Основные настройки
│   ├── models/        # SQLAlchemy модели
│   ├── schemas/       # Pydantic схемы
│   ├── repositories/  # Паттерн Repository
│   ├── routes/        # Маршруты API
│   ├── services/      # Бизнес-логика
│   ├── migrations/    # Миграции (Alembic)
│   └── main.py        # Точка входа
├── .env.template      # Шаблон переменных окружения
├── docker-compose.yml # Docker Compose конфиг
└── requirements/      # Зависимости
```

## 🐳 Docker команды

```bash
# Запуск в фоновом режиме
$ docker-compose up -d

# Остановка контейнеров
$ docker-compose down

# Просмотр логов
$ docker-compose logs -f

# Пересборка образов
$ docker-compose build --no-cache
```

## 🔄 Миграции

```bash
# Создать новую миграцию
$ docker-compose exec web alembic revision --autogenerate -m "Description"

# Применить миграции
$ docker-compose exec web alembic upgrade head

# Откатить миграцию
$ docker-compose exec web alembic downgrade -1
```

## Лицензия

MIT License © 2024 [Eruslanov Ivan]

```
Иконки автоматически подтягиваются с сервиса [Shields.io](https://shields.io/). Вы можете:

1. Обновить версии в бейджах, изменив цифры в URL
2. Добавить новые технологии через [кастомные бейджи](https://shields.io/category/version)
3. Изменить цвета через hex-коды (например: `?color=00C7B7`)
4. Добавить логотипы из [проекта Simple Icons](https://simpleicons.org/)

Для создания своих бейджей можно использовать конструктор:
https://shields.io/badges
```
