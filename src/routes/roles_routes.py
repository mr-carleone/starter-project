# src/routes/roles.py
from fastapi import APIRouter, Depends
from src.services.role_service import RoleService
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_db
from src.schemas.user_schema import RoleBase

router = APIRouter(prefix="/api/v1/roles", tags=["roles"])


@router.get("/", response_model=list[RoleBase])
async def get_roles(db: AsyncSession = Depends(get_db)):
    async with db:
        service = RoleService(db)
        return await service.get_all_roles()
