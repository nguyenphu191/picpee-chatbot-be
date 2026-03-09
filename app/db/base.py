from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings


settings = get_settings()

# Engine & Session cho metadata DB (documents, chunks, ...)
engine = create_engine(settings.db_url, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency dùng trong FastAPI để lấy session DB:

    from fastapi import Depends
    from sqlalchemy.orm import Session
    from app.db.base import get_db

    def endpoint(db: Session = Depends(get_db)):
        ...
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

