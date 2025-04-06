import logging
import os
from dotenv import load_dotenv

load_dotenv("./.env")
IS_DEV_MODE = os.getenv("DEV_MODE")

# config your fastapi app
app_config = {
    "project_name": "project_name",
    "project_version": "1.0.0",
    "project_description": "project_description",
}

# config your logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# config your database engine based on your provider
database_config = {"url": ""}


def database_url_config():
    if IS_DEV_MODE == "True":
        logger.info(f"DEV_MODE is set to {IS_DEV_MODE}")
        database_config["url"] = "sqlite:///dev.db"
        logger.info(f"Database engine using SQLite")
    else:
        logger.info(f"DEV_MODE is not set, using production database")
        database_config["url"] = os.getenv("SUPABASE_CONNECTION_STRING")
        logger.info(f"Database engine using Supabase PostgreSQL")


jwt_config = {
    "secret_key": os.getenv("JWT_SECRET_KEY"),
    "algorithm": "HS256",
    # 24 hours
    "access_token_expire_minutes": 60 * 24,
}
