# src/repositories/__init__.py
from .user_repository import UserRepository
from .role_repository import RoleRepository

__all__ = ["UserRepository", "RoleRepository"]
