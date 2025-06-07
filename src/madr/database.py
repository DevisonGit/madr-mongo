from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.madr.settings import Settings


def get_engine():
    return create_engine(Settings().DATABASE_URL)


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session
