# src/routes/init_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from src.services.initial_data_service import InitialDataService
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import (get_db)
from src.core.auth_dependencies import required_roles
from src.core.config import settings

router = APIRouter(prefix="/api/v1/init/user", tags=["Iinit Super User"])

@router.post(
    "/",
    include_in_schema=False,
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def create_user(session: AsyncSession = Depends(get_db)):
    if settings.DB_MODE != 'real':
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Initialization not allowed in this mode")
    initial_service = InitialDataService(session)
    try:
        await initial_service.initialize()
        return {"message": "Initialization completed successfully"}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Initialization failed: {str(e)}")
