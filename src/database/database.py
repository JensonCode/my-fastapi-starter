from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import database_config, database_url_config

database_url_config()
engine = create_engine(database_config["url"])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
