# src/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.core.security import create_access_token
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import TokenResponse
from sqlalchemy.orm import Session
from src.core.database import get_db

router = APIRouter(
    tags=["Authentication"],
    prefix="/api/v1/auth"
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User authentication",
    description="Authenticate user and obtain access token",
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect username or password"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Authentication process failed"}
                }
            }
        }
    }
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and generate JWT token

    Parameters:
    - **username**: User's login identifier
    - **password**: User's password

    Returns:
    - JWT access token for authorized requests
    """
    user_repo = UserRepository(db)

    try:
        user = user_repo.authenticate_user(
            form_data.username,
            form_data.password
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication process failed"
        ) from e

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    try:
        return {
            "access_token": create_access_token(user.id),
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token generation failed"
        ) from e
