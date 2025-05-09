# src/core/dependencies.py
from src.core.unit_of_work import UnitOfWork
from src.core.database import adb
from typing import AsyncGenerator


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with adb.get_session() as session:
        uow = UnitOfWork(session)
        yield uow
