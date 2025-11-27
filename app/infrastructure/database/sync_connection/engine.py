from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import Base
from config.settings import Config

config = Config()

engine = create_engine(config.DATABASE_URL, echo=True)
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
