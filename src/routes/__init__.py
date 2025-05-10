# src/routes/__init__.py
from .healthcheck_routes import router as healthcheck_router
from .auth_routes import router as auth_router
from .roles_routes import router as roles_router
from .users_routes import router as users_router
from .init_routes import router as init_router
from .swagger_routes import router as swagger_router

__all__ = [
    'healthcheck_router',
    'auth_router',
    'roles_router',
    'users_router',
    'init_router',
    'swagger_router'
]
