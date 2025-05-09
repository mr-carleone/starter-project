# src/services/initial_data_service.py
from src.core.config import settings
from src.core.unit_of_work import UnitOfWork
from src.services.role_service import RoleService
from src.services.user_service import UserService


class InitialDataService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def initialize(self):
        async with self.uow:
            # Инициализация ролей
            role_service = RoleService(self.uow.session)
            if not await role_service.get_all_roles():
                await role_service.create_role("FULL_ACCESS")
                await role_service.create_role("INTEGRATION_ROLE")

            # Инициализация администратора
            user_service = UserService(self.uow.session)
            if not await user_service.get_user_by_username(
                settings.INITIAL_USER_USERNAME
            ):
                role = await role_service.get_role_by_name(settings.INITIAL_USER_ROLE)
                await user_service.create_admin_user(
                    username=settings.INITIAL_USER_USERNAME,
                    email=settings.INITIAL_USER_EMAIL,
                    phone=settings.INITIAL_USER_PHONE,
                    password=settings.INITIAL_USER_PASSWORD,
                    role_id=role.id,
                )
            await self.uow.commit()
