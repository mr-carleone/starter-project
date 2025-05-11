# tests/tests/healthcheck.py
from fastapi import status

def test_healthcheck_endpoint(client):
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}

def test_db_healthcheck(client, mock_db):
    mock_db.async_session().execute.return_value.scalar.return_value = 1

    response = client.get("/api/v1/healthcheck/db")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "OK"
