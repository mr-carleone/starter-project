# src/routes/users_routes.py
from fastapi import APIRouter, Depends, status
from src.services.user_service import UserService
from src.schemas.user_schema import UserCreate, UserUpdate, UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_db
from src.core.auth_dependencies import required_roles
from uuid import UUID

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post(
    "/",
    response_model=UserInDB,
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.create_user(user_data)


@router.get(
    "/",
    response_model=list[UserInDB],
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.get_all_users()


@router.get(
    "/{user_id}",
    response_model=UserInDB,
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.get_user_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserInDB,
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def update_user(
    user_id: UUID, update_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.update_user(user_id, update_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(required_roles(["FULL_ACCESS"]))],
)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    await service.delete_user(user_id)
    return {"status": "success", "message": "User deleted successfully"}
