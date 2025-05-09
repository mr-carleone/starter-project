# src/core/exceptions.py
from fastapi import HTTPException, status


class AppError(HTTPException):
    def __init__(self, message: str, code: int):
        super().__init__(status_code=code, detail=message)


class NotFoundError(AppError):
    def __init__(self, entity: str):
        super().__init__(f"{entity} not found", status.HTTP_404_NOT_FOUND)


class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_409_CONFLICT)


class AuthError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)
