# src/entities/user.py
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.sql import text

from src.models.base import Base
from src.models.mixins import AuditMixin


class Role(Base, AuditMixin):
    __tablename__ = "sec_role"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        comment="Уникальный идентификатор роли",
    )

    name = Column(String(50), unique=True, nullable=False, comment="Наименование роли")

    users = relationship("User", back_populates="role", cascade="all, delete-orphan")


class User(Base, AuditMixin):
    __tablename__ = "sec_user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        comment="Уникальный идентификатор пользователя",
    )

    username = Column(
        String(50), unique=True, nullable=False, comment="Логин пользователя"
    )

    email = Column(
        String(100), unique=True, nullable=False, comment="Электронная почта"
    )

    phone = Column(String(20), unique=True, nullable=False, comment="Номер телефона")

    hashed_password = Column(String(255), nullable=False, comment="Хэшированный пароль")

    is_active = Column(
        Boolean, default=False, nullable=False, comment="Активен ли пользователь"
    )

    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sec_role.id"),
        nullable=False,
        comment="Ссылка на роль пользователя",
    )

    role = relationship("Role", back_populates="users", lazy="joined")
