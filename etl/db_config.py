from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv
from etl.logger import logging
import os


def load_db_config():
    # Load environment variables from .env file
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    # Get the database URL from environment variables
    db_url = os.getenv('DB_URL')

    if not db_url:
        raise ValueError("Database URL not found in environment variables.")

    return db_url


def create_db_engine():
    db_url = load_db_config()
    engine = create_engine(db_url)
    return engine


logging.info(
    f"Database Engine created successfully with URL: {load_db_config()}")
