# src/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from src.core.config import settings
from src.core.logging import setup_logging
import logging
from src.core.initial_data import init_default_data
from src.routes import healthcheck
from src.routes import auth
from src.routes import roles
from src.routes import users

setup_logging()

logger = logging.getLogger(__name__)
logger.info(f"ENV: {settings.ENV}, LOG_LEVEL: {settings.LOG_LEVEL}")

# Инициализация данных
init_default_data()

app = FastAPI(
    title="Transport Logistics API",
    description="API для управления автомобильными и железнодорожными отгрузками",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight": True,
        "docExpansion": "none",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "customSiteTitle": "Transport Logistics API",
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


app.include_router(healthcheck.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
