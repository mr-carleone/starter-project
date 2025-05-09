# src/routes/roles.py
from fastapi import APIRouter, Depends
from src.services.role_service import RoleService
from src.core.unit_of_work import UnitOfWork
from src.core.dependencies import get_uow
from src.schemas.user_schema import RoleBase

router = APIRouter(prefix="/api/v1/roles", tags=["roles"])


@router.get("/", response_model=list[RoleBase])
async def get_roles(uow: UnitOfWork = Depends(get_uow)):
    async with uow:
        service = RoleService(uow.session)
        return await service.get_all_roles()
