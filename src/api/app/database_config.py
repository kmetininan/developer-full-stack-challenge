# database_config.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

# Load environment variables
config = dotenv_values(".env")

# Configurations
DATABASE_URL = config["DATABASE_URL"]
JWT_SECRET_KEY = config["JWT_SECRET_KEY"]
SECRET_KEY = config["SECRET_KEY"]

# Database engine
engine = create_engine(DATABASE_URL)

# Session maker instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

