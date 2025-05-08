# srs/schemas/health_schema.py
from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    db_mode: str | None = None
    db_connection: str | None = None

    class Config:
        json_schema_extra = {
            "example": {"status": "OK", "db_mode": "mock", "db_connection": "success"}
        }
