# src/core/initial_data.py
from src.core.database import get_db
from src.schemas.user_schema import UserCreate
from src.repositories.user_repository import UserRepository
from src.repositories.role_repository import RoleRepository
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


def init_default_data():
    if settings.DB_MODE != "real":
        return

    db = get_db()

    try:
        # Создаем роли если их нет
        role_repo = RoleRepository(db)
        if not role_repo.get_all_roles():
            role_repo.create_role(name="FULL_ACCESS")
            role_repo.create_role(name="INTEGRATION_ROLE")
            logger.info("Default roles created")

        # Создаем администратора
        user_repo = UserRepository(db)
        if not user_repo.get_user_by_username(settings.INITIAL_USER_USERNAME):
            role = role_repo.get_role_by_name(settings.INITIAL_USER_ROLE)

            user_data = UserCreate(
                username=settings.INITIAL_USER_USERNAME,
                email=settings.INITIAL_USER_EMAIL,
                phone=settings.INITIAL_USER_PHONE,
                password=settings.INITIAL_USER_PASSWORD,
            )

            user_repo.create_user(user_data, role_id=role.id)
            logger.info("Initial admin user created")

    except Exception as e:
        logger.error(f"Data initialization failed: {str(e)}")
        db.rollback()
    finally:
        db.close()
