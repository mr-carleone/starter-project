# src/core/logging.py
import logging
from colorlog import ColoredFormatter
from src.core.config import settings


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # Настройка для SQLAlchemy
    sqlalchemy_logger = logging.getLogger('sqlalchemy')
    sqlalchemy_logger.setLevel(logging.WARNING if settings.ENV == 'prod' else logging.INFO)

    # Отключаем логирование пула соединений
    logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
    logging.getLogger('sqlalchemy.engine').setLevel(
        logging.WARNING if settings.ENV == 'prod' else logging.INFO
    )

    if settings.ENV == "dev":
        # Color format for development
        formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)-8s %(name)s %(purple)s%(filename)s:%(lineno)d%(reset)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    else:
        # JSON format for production
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "file": "%(filename)s:%(lineno)d", "message": "%(message)s"}'
        )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Убираем дублирование логов от uvicorn
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").addHandler(handler)
