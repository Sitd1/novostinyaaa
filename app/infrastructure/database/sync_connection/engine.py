from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.models import Base
from app.config import database_config


engine = create_engine(database_config.url_asyncpg, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    SessionLocal()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
