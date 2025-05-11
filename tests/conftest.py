# tests/conftest.py
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import adb

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_db(monkeypatch):
    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()
    monkeypatch.setattr(adb, "get_session", lambda: mock_session)
    return mock_session

@pytest.fixture
def client():
    return TestClient(app)
