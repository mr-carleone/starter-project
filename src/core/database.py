# src/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.is_connected = False

    def connect(self):
        if settings.DB_MODE == "real":
            try:
                self.engine = create_engine(settings.DATABASE_URL)
                self.SessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self.engine
                )
                self.is_connected = True
            except Exception as e:
                logger.error(f"Database connection error: {e}")
                self.is_connected = False
        else:
            logger.info("Using mock database")
            self.is_connected = False

    def get_session(self):
        if self.is_connected:
            return self.SessionLocal()
        return MockSession()

class MockSession:
    """Заглушка для сессии БД"""
    def __getattr__(self, name):
        def mock_method(*args, **kwargs):
            print(f"Mock DB method called: {name}")
            return None
        return mock_method

db = Database()
db.connect()

def get_db():
    return db.get_session()
