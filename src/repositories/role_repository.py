# src/repositories/role_repository.py
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.user import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_role(self, name: str):
        role = Role(name=name)
        self.db.add(role)
        self.db.commit()
        return role

    def get_role_by_name(self, name: str) -> Role:
        return self.db.query(Role).filter(Role.name == name).first()

    def get_all_roles(self) -> List[Role]:
        return self.db.query(Role).all()
