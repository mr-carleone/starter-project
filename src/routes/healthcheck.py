# src/routes/healthcheck.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.config import settings
from src.schemas.health_schema import HealthCheckResponse

router = APIRouter(tags=["System Health Checks"], prefix="/api/v1/healthcheck/db")


@router.get(
    "/",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Check database connection status",
    description="Performs a basic database health check by executing a simple SQL query.",
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully connected to database or using mock mode",
            "content": {
                "application/json": {
                    "examples": {
                        "mock_mode": {"value": {"status": "OK", "db_mode": "mock"}},
                        "real_connection": {
                            "value": {"status": "OK", "db_connection": "success"}
                        },
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Database connection failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Database connection failed: <error_details>"}
                }
            },
        },
    },
)
async def db_healthcheck(db: Session = Depends(get_db)):
    """
    Performs a health check of the database connection.

    Returns:
    - Standard health status with DB mode information when using mock
    - Database connection status for real database mode

    Raises:
    - HTTPException 500: If database connection test fails
    """
    if settings.DB_MODE == "mock":
        return {"status": "OK", "db_mode": "mock"}

    try:
        db.execute(text("SELECT 1"))
        return {"status": "OK", "db_connection": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )
