# src/routes/roles.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.user_schema import RoleBase
from src.core.database import get_db
from src.repositories.role_repository import RoleRepository

router = APIRouter(
    prefix="/api/v1/roles",
    tags=["roles"]
)

@router.get("/", response_model=list[RoleBase])
def get_roles(db: Session = Depends(get_db)):
    repo = RoleRepository(db)
    return repo.get_all_roles()
