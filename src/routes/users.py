# src/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from src.services.user_service import UserService
from src.schemas.user_schema import UserCreate, UserInDB
from src.core.unit_of_work import UnitOfWork
from src.core.dependencies import get_uow

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        async with uow:
            service = UserService(uow.session)
            return await service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
