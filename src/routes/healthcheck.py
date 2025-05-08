# src/routes/healthcheck.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.config import settings

router = APIRouter(tags=["Healthcheck"])

@router.get("/healthcheck/db")
async def db_healthcheck(db: Session = Depends(get_db)):
    if settings.DB_MODE == "mock":
        return {"status": "OK", "db_mode": "mock"}

    try:
        db.execute(text("SELECT 1"))
        return {"status": "OK", "db_connection": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
