from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..core.config import get_settings

settings = get_settings()

engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 