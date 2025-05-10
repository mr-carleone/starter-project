# src/services/role_service.py
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.services.base_service import BaseService
from src.repositories.role_repository import AsyncRoleRepository
from src.schemas.user_schema import RoleResponse
from src.core.exceptions import NotFoundError, ConflictError
from src.core.cache import role_cache
from cachetools import cached


class RoleService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = AsyncRoleRepository(session)

    @classmethod
    async def create(cls, session: AsyncSession):
        return cls(session)

    async def get_all_roles(self) -> List[RoleResponse]:
        roles = await self.repo.get_all_roles()
        return [RoleResponse.model_validate(role) for role in roles]

    async def create_role_without_commit(
        self, name: str, current_user: str
    ) -> RoleResponse:
        try:
            role = await self.repo.create_role(name, current_user)
            return RoleResponse.model_validate(role)
        except IntegrityError:
            raise ValueError("Role name must be unique not duplicate")

    @cached(role_cache)
    async def get_role_by_id(self, role_id: UUID) -> RoleResponse:
        role = await self.repo.get_role_by_id(role_id)
        if not role:
            raise NotFoundError(f"Role with id {role_id} not found")
        return RoleResponse.model_validate(role)

    async def get_role_by_name(self, role_name: str) -> RoleResponse:
        role = await self.repo.get_role_by_name(role_name)
        if not role:
            raise NotFoundError(f"Role with name {role_name} not found")
        return RoleResponse.model_validate(role)

    async def create_role(self, name: str, current_user: str) -> RoleResponse:
        try:
            role = await self.repo.create_role(name, current_user)
            await self.commit()
            return RoleResponse.model_validate(role)
        except IntegrityError:
            await self.rollback()
            raise ValueError("Role name must be unique")

    async def update_role(
        self, role_id: UUID, name: str, current_user: str
    ) -> RoleResponse:
        try:
            role = await self.repo.update_role(role_id, name, current_user)
            await self.commit()
            return RoleResponse.model_validate(role)
        except IntegrityError:
            await self.rollback()
            raise ConflictError("Role name must be unique")

    async def delete_role(self, role_id: UUID) -> bool:
        result = await self.repo.delete_role(role_id)
        if not result:
            raise NotFoundError("Role")
        return True
