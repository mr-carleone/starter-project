# src/routes/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.schemas.user_schema import UserCreate, UserInDB
from src.repositories.user_repository import UserRepository
from src.core.database import get_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, role_id: UUID, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    # Проверяем существование роли
    if not repo.role_exists(role_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {role_id} not found",
        )

    try:
        return repo.create_user(user, role_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
