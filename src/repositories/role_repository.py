# src/repositories/role_repository.py
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.entities.user import Role


class AsyncRoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role_by_id(self, role_id: UUID) -> Role:
        result = await self.db.execute(select(Role).filter(Role.id == role_id))
        return result.scalars().first()

    async def get_role_by_name(self, name: str) -> Role:
        result = await self.db.execute(select(Role).filter(Role.name == name))
        return result.scalars().first()

    async def create_role(self, name: str, current_user: str) -> Role:
        role = Role(name=name, created_by=current_user)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def get_all_roles(self) -> List[Role]:
        result = await self.db.execute(select(Role))
        return result.scalars().all()

    async def update_role(self, role_id: UUID, name: str, updated_by: str) -> Role:
        role = await self.get_role_by_id(role_id)
        if not role:
            raise ValueError("Role not found")

        role.name = name
        role.updated_by = updated_by
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def delete_role(self, role_id: UUID) -> bool:
        role = await self.db.get(Role, role_id)
        if not role:
            return False
        await self.db.delete(role)
        await self.db.commit()
        return True
