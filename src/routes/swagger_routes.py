# src/routes/swagger.py
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter()

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Test Logistics API - Swagger UI",
        swagger_css_url="/static/swagger/custom_swagger.css",
        swagger_ui_parameters={
            "syntaxHighlight": True,
            "docExpansion": "none",
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": True
        },
    )
