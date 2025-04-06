from alembic.config import Config
from alembic import command
from alembic.util.exc import CommandError
from ..config import logger
import os


def check_migrations():
    try:
        alembic_cfg = Config(
            os.path.join(os.path.dirname(__file__), "../../alembic.ini")
        )

        try:
            command.check(alembic_cfg)
            logger.info("Migrations are up to date")
        except CommandError as e:
            if "Target database is not up to date" in str(e):
                logger.warning("Database is not up to date. Applying migrations...")

                command.upgrade(alembic_cfg, "head")
                logger.info("Migrations applied successfully")
            else:
                logger.warning(f"Migration check warning: {e}")
    except Exception as e:
        logger.error(f"Migration check failed: {e}")
        logger.error("Continuing without migrations")
