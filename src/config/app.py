# src/config/app.py
from fastapi import FastAPI
from src.routes import (
    healthcheck_router,
    auth_router,
    roles_router,
    users_router,
    init_router,
    swagger_router
)

def create_app() -> FastAPI:
    return FastAPI(
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
        }
    )

def configure_routers(app: FastAPI) -> None:
    routers = [
        swagger_router,
        healthcheck_router,
        auth_router,
        users_router,
        roles_router,
        init_router
    ]

    for router in routers:
        app.include_router(router)
