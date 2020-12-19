import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


DATABASE_URL = os.getenv("DATABASE_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT")

engine = None
session = None

if ENVIRONMENT == "production":
    # use postgresql
    engine = create_engine(DATABASE_URL)
    logger.info("Created db engine with url: %s", DATABASE_URL)

if ENVIRONMENT == "development":
    # use sqlite
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    logger.info("Created testing db engine with url: %s", DATABASE_URL)


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Create a Base class for models
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
