import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DATABASE_URL', default='sqlite+aiosqlite:///./fastapi.db')
SECRET = os.getenv('SECRET', default='secret')
BASE_DIR = Path(__file__).parent
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
FIRST_SUPERUSER_EMAIL = os.getenv('FIRST_SUPERUSER_EMAIL', default='superuser@user.ru')
FIRST_SUPERUSER_PASSWORD = os.getenv('FIRST_SUPERUSER_PASSWORD', default='superuser')
