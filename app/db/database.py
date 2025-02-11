from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user_test:123456@localhost/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(engine)
Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db

    finally:
        db.close()
