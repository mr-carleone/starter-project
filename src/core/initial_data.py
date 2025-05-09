# src/core/initial_data.py
from src.core.database import adb
from src.schemas.user_schema import UserCreate
from src.repositories.user_repository import AsyncUserRepository
from src.repositories.role_repository import AsyncRoleRepository
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


async def async_init_default_data():
    if settings.DB_MODE != "real":
        return

    async with adb.get_session() as session:
        try:
            # Roles
            role_repo = AsyncRoleRepository(session)
            if not await role_repo.get_all_roles():
                await role_repo.create_role(name="FULL_ACCESS")
                await role_repo.create_role(name="INTEGRATION_ROLE")
                logger.info("Default roles created")

            # Admin user
            user_repo = AsyncUserRepository(session)
            if not await user_repo.get_user_by_username(settings.INITIAL_USER_USERNAME):
                role = await role_repo.get_role_by_name(settings.INITIAL_USER_ROLE)

                user_data = UserCreate(
                    username=settings.INITIAL_USER_USERNAME,
                    email=settings.INITIAL_USER_EMAIL,
                    phone=settings.INITIAL_USER_PHONE,
                    password=settings.INITIAL_USER_PASSWORD,
                    role_id=role.id,
                )

                await user_repo.create_user(user_data, role.id)
                logger.info("Initial admin user created")

            await session.commit()
        except Exception as e:
            logger.error(f"Data initialization failed: {str(e)}")
            await session.rollback()
