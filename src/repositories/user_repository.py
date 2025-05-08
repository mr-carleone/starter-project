# src/repositories/user_repository.py
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.entities.user import User, Role
from src.schemas.user_schema import UserCreate
from src.core.logging import setup_logging
import logging

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def role_exists(self, role_id: UUID) -> bool:
        return self.db.query(Role).filter(Role.id == role_id).first() is not None

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user_data: UserCreate, role_id: UUID) -> User:
        logger.info(user_data)
        hashed_password = pwd_context.hash(user_data.password)
        logger.info(hashed_password)

        user = User(
            username=user_data.username,
            email=user_data.email,
            phone=user_data.phone,
            hashed_password=hashed_password,
            role_id=role_id
        )

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            if "username" in str(e):
                raise ValueError("Username already exists")
            elif "email" in str(e):
                raise ValueError("Email already exists")
            elif "phone" in str(e):
                raise ValueError("Phone number already exists")
            raise ValueError("Database integrity error")
