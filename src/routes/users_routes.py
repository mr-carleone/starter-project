# src/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from src.services.user_service import UserService
from src.schemas.user_schema import UserCreate, UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        async with db:
            service = UserService(db)
            return await service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
