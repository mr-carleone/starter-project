# src/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.core.security import create_access_token
from src.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from src.core.database import get_db

router = APIRouter(tags=["auth"])


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": create_access_token(user.id), "token_type": "bearer"}
