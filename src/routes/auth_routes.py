# src/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import get_db
from src.schemas.auth_schema import TokenResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Authentication"], prefix="/api/v1/auth")


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
                        "token_type": "bearer",
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect username or password"}
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Authentication process failed"}
                }
            },
        },
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate user and generate JWT token

    Parameters:
    - **username**: User's login identifier
    - **password**: User's password

    Returns:
    - JWT access token for authorized requests
    """

    try:
        logger.info(f"Attempting to authenticate user: {form_data.username}")
        async with db:
            service = AuthService(db)
            logger.info("AuthService initialized")
            return await service.authenticate(form_data.username, form_data.password)
    except ValueError as ve:
        logger.error(f"Authentication failed: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        ) from ve
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication process failed",
        ) from e
