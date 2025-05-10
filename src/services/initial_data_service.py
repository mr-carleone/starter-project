# src/services/initial_data_service.py
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user_schema import UserCreate
from src.services.role_service import RoleService
from src.services.user_service import UserService
from src.core.exceptions import NotFoundError
import logging

logger = logging.getLogger(__name__)


class InitialDataService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize(self):
        try:
            # Инициализация ролей
            role_service = RoleService(self.session)
            existing_roles = await role_service.get_all_roles()

            if not existing_roles:
                logger.info("Creating default roles")
                await role_service.create_role_without_commit("FULL_ACCESS", "system")
                await role_service.create_role_without_commit(
                    "INTEGRATION_ROLE", "system"
                )
                await self.session.commit()

            # Инициализация администратора
            user_service = UserService(self.session)
            try:
                await user_service.get_user_by_username(settings.INITIAL_USER_USERNAME)
                logger.debug("Admin user already exists")
            except NotFoundError:
                logger.info("Creating initial admin user")
                role = await role_service.get_role_by_name(settings.INITIAL_USER_ROLE)

                await user_service.create_user(
                    user_data=UserCreate(
                        username=settings.INITIAL_USER_USERNAME,
                        email=settings.INITIAL_USER_EMAIL,
                        phone=settings.INITIAL_USER_PHONE,
                        password=settings.INITIAL_USER_PASSWORD,
                        role_id=role.id,
                        is_active=True,
                    ),
                    current_user=settings.INITIAL_USER_CREATED_BY,
                )

                logger.info("Admin user created successfully")

        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            await self.session.rollback()
            raise
