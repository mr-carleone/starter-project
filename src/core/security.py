# src/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.core.config import settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создание JWT токена
    :param subject: Идентификатор пользователя
    :param expires_delta: Время жизни токена
    :return: Подписанный JWT токен
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    try:
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except jwt.JWTError as e:  # Используем JWTError для обработки ошибок
        raise ValueError("Token creation error") from e


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed.startswith("$argon2"):
        raise ValueError("Legacy hash format detected")
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_token(token: str) -> dict:
    """
    Верификация JWT токена
    :param token: JWT токен
    :return: Декодированные данные токена
    :raises JWTError: Если токен невалиден
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise JWTError("Invalid token") from e
