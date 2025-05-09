# src/services/role_service.py
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.services.base_service import BaseService
from src.repositories.role_repository import AsyncRoleRepository
from src.schemas.user_schema import RoleBase
from src.core.exceptions import NotFoundError


class RoleService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = AsyncRoleRepository(session)

    @classmethod
    async def create(cls, session: AsyncSession):
        return cls(session)

    async def get_all_roles(self) -> List[RoleBase]:
        roles = await self.repo.get_all_roles()
        return [RoleBase.model_validate(role) for role in roles]

    async def create_role_without_commit(self, name: str) -> RoleBase:
        try:
            role = await self.repo.create_role(name)
            return RoleBase.model_validate(role)
        except IntegrityError:
            raise ValueError("Role name must be unique")

    async def get_role_by_id(self, role_id: UUID) -> RoleBase:
        role = await self.repo.get_role_by_id(role_id)
        if not role:
            raise NotFoundError(f"Role with id {role_id} not found")
        return RoleBase.model_validate(role)

    async def get_role_by_name(self, role_name: str) -> RoleBase:
        role = await self.repo.get_role_by_name(role_name)
        if not role:
            raise NotFoundError(f"Role with name {role_name} not found")
        return RoleBase.model_validate(role)

    async def create_role(self, name: str) -> RoleBase:
        try:
            role = await self.repo.create_role(name)
            await self.commit()
            return RoleBase.model_validate(role)
        except IntegrityError:
            await self.rollback()
            raise ValueError("Role name must be unique")
