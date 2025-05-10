# src/routes/init_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from src.services.initial_data_service import InitialDataService
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_db
from src.core.config import settings

router = APIRouter(prefix="/api/v1/init", tags=["Iinit Super User"])

init_header = APIKeyHeader(name="X-Init-Token")


@router.post("/")
async def create_user(
    session: AsyncSession = Depends(get_db), token: str = Depends(init_header)
):
    if settings.DB_MODE != "real":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Initialization not allowed in this mode"
        )
    initial_service = InitialDataService(session)
    try:
        if token != settings.INITIAL_USER_TOKEN:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid token")
        await initial_service.initialize()
        return {"message": "Initialization completed successfully"}
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Initialization failed: {str(e)}",
        )
