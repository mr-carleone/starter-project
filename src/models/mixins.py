# src/models/mixins.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func


class AuditMixin:
    """
    Миксин с общими аудиторскими полями для всех моделей
    Важно: НЕ наследуем от Base!
    """

    version = Column(Integer, nullable=False, default=1)
    create_ts = Column(TIMESTAMP(timezone=True), server_default=func.now())
    created_by = Column(String(50))
    update_ts = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    updated_by = Column(String(50))
    delete_ts = Column(TIMESTAMP(timezone=True))
    deleted_by = Column(String(50))

    @staticmethod
    def _set_audit_fields(mapper, connection, target):
        # Убираем автоматическую установку, будем управлять вручную
        pass
