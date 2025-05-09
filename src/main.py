from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from src.routes import healthcheck_routes
from src.routes import auth_routes
from src.routes import roles_routes
from src.routes import users_routes
from src.core.config import settings
from src.core.logging import setup_logging
from src.core.database import adb
from src.services.initial_data_service import InitialDataService
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
    async with adb.get_session() as session:
        initial_service = InitialDataService(session)
        await initial_service.initialize()

    logger.info("Initial data setup completed")

    yield

    # Логика завершения (опционально)
    logger.info("Shutting down application...")
    await adb.engine.dispose()
    logger.info("Database connection closed")


app = FastAPI(
    lifespan=lifespan,
    title="Test Logistics API",
    description="API для начальной разработки",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight": True,
        "docExpansion": "none",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "customSiteTitle": "Test Logistics API",
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
app.include_router(healthcheck_routes.router)
app.include_router(auth_routes.router)
app.include_router(users_routes.router)
app.include_router(roles_routes.router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
