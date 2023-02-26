import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

from .constants import (BASE_DIR, DB_URL, DT_FORMAT, FIRST_SUPERUSER_EMAIL,
                        FIRST_SUPERUSER_PASSWORD, LOG_FORMAT, SECRET)

load_dotenv()


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Сервис для поддержки котиков!'
    database_url: str = DB_URL
    secret: str = SECRET
    first_superuser_email: Optional[EmailStr] = FIRST_SUPERUSER_EMAIL
    first_superuser_password: Optional[str] = FIRST_SUPERUSER_PASSWORD

    class Config:
        env_file = '.env'


def configure_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'cat_charity_fund_logger.log'
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 ** 6,
        backupCount=5,
        encoding="UTF-8"
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.ERROR,
        handlers=(rotating_handler, logging.StreamHandler())
    )
