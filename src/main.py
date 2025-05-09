from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from src.routes import healthcheck
from src.routes import auth
from src.routes import roles
from src.routes import users
from src.core.config import settings
from src.core.logging import setup_logging
from src.core.database import adb
from src.core.initial_data import initialize_default_data
import logging

# Настройка логгера должна быть первой
setup_logging()

logger = logging.getLogger(__name__)
logger.info(f"ENV: {settings.ENV}, LOG_LEVEL: {settings.LOG_LEVEL}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Стартовая логика
    logger.info("Starting application...")

    # Подключение к БД
    await adb.connect()
    logger.info("Database connection established")

    # Инициализация данных
    await initialize_default_data()
    logger.info("Initial data setup completed")

    yield

    # Логика завершения (опционально)
    logger.info("Shutting down application...")
    await adb.engine.dispose()
    logger.info("Database connection closed")


app = FastAPI(
    lifespan=lifespan,
    title="Transport Logistics API",
    description="API для управления автомобильными и железнодорожными отгрузками",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight": True,
        "docExpansion": "none",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "customSiteTitle": "Transport Logistics API",
        "swagger_favicon_url": "/static/favicon.ico",
    },
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_css_url="/static/swagger/custom_swagger.css",
        swagger_ui_parameters=app.swagger_ui_parameters,
    )


# Подключение роутеров
app.include_router(healthcheck.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
