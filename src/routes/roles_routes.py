# src/routes/roles.py
from fastapi import APIRouter, Depends, status
from src.services.role_service import RoleService
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_db
from src.schemas.user_schema import RoleResponse, RoleUpdate, RoleCreate
from src.core.auth_dependencies import required_roles, get_current_user_username
from uuid import UUID

router = APIRouter(prefix="/api/v1/roles", tags=["roles"])


@router.get(
    "/",
    response_model=list[RoleResponse],
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def get_roles(db: AsyncSession = Depends(get_db)):
    service = RoleService(db)
    return await service.get_all_roles()


@router.post(
    "/",
    response_model=RoleResponse,
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user_username),
):
    service = RoleService(db)
    return await service.create_role(role_data.name, current_user)


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def update_role(
    role_id: UUID,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user_username),
):
    service = RoleService(db)
    return await service.update_role(role_id, role_data.name, current_user)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def delete_role(role_id: UUID, db: AsyncSession = Depends(get_db)):
    service = RoleService(db)
    await service.delete_role(role_id)
    return {"status": "success", "message": "Role deleted successfully"}
