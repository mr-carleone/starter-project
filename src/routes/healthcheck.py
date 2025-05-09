# src/routes/healthcheck_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.health_schema import HealthCheckResponse
from src.services.healthcheck_service import HealthcheckService
from src.core.unit_of_work import UnitOfWork
from src.core.dependencies import get_uow

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
async def db_healthcheck(uow: UnitOfWork = Depends(get_uow)):
    """
    Performs a health check of the database connection.

    Returns:
    - Standard health status with DB mode information when using mock
    - Database connection status for real database mode

    Raises:
    - HTTPException 500: If database connection test fails
    """
    try:
        async with uow:
            service = HealthcheckService(uow.session)
            return await service.check_db_health(uow)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
