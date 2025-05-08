# src/routes/healthcheck.py
from .healthcheck import router as healthcheck_router
from .auth import router as auth_router
from .roles import router as role_router
from .users import router as user_router

__all__=["healthcheck_router", "auth_router", "role_router", "user_router"]
