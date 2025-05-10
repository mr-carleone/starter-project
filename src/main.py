from fastapi.staticfiles import StaticFiles
from src.config.app import create_app, configure_routers
from src.utils.lifespan import lifespan
from src.core.logging import setup_logging

# Настройка логгера должна быть первой
setup_logging()

app = create_app()
app.mount("/static", StaticFiles(directory="src/static"), name="static")
configure_routers(app)

# Добавление lifespan
app.router.lifespan_context = lifespan
