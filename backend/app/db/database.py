import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Read the database connection string from the environment.
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# Configure a reusable SQLAlchemy session factory for request-scoped sessions.
session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    """Yield a request-scoped database session and close it after the request."""
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
