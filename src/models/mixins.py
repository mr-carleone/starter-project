# src/models/mixins.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, event, text
from sqlalchemy.sql import func
from src.core.config import settings


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
        if not target.created_by:
            target.created_by = settings.SYSTEM_USERNAME
        if not target.updated_by:
            target.updated_by = settings.SYSTEM_USERNAME

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_insert", AuditMixin._set_audit_fields)
        event.listen(cls, "before_update", AuditMixin._set_audit_fields)
