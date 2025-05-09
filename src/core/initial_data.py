# src/core/initial_data.py
from src.services.initial_data_service import InitialDataService
from src.core.unit_of_work import UnitOfWork
from src.core.database import adb
from src.core.config import settings


async def initialize_default_data():
    if settings.DB_MODE != "real":
        return

    async with adb.get_session() as session:
        uow = UnitOfWork(session)
        service = InitialDataService(uow)
        await service.initialize()
