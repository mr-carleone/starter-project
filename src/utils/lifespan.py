# src/utils/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.database import adb
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Database connection establishing...")
        await adb.connect()
        logger.info("Database connection established")
        yield
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        logger.info("Shutting down application...")
        if adb.engine:
            await adb.engine.dispose()
