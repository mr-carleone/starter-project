# src/routes/healthcheck.py
from .healthcheck_routes import router as healthcheck_router
from .auth_routes import router as auth_router
from .roles_routes import router as role_router
from .users_routes import router as user_router

__all__ = ["healthcheck_router", "auth_router", "role_router", "user_router"]
