# src/core/auth_dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_db
from src.core.exceptions import NotFoundError
from src.core.security import verify_token
from src.services.user_service import UserService
from src.schemas.user_schema import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        service = UserService(db)
        user = await service.get_user_by_id(user_id)
        return user
    except (JWTError, NotFoundError):
        raise credentials_exception


def required_roles(roles: list[str]):
    async def checker(current_user: UserInDB = Depends(get_current_user)):
        if current_user.role.name not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return current_user

    return checker

async def get_current_user_username(current_user: UserInDB = Depends(get_current_user)) -> str:
    return current_user.username
