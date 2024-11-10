from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(autocommit=False, expire_on_commit=False,bind=engine)
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

db = Annotated[Session, Depends(get_db)]