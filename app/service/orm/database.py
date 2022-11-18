import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


database_url = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ.get("DB_USER", "test_user"),
    os.environ.get("DB_PASSWORD", "test"),
    os.environ.get("DB_HOST", "localhost"),
    os.environ.get("DB_PORT", "5437"),
    os.environ.get("DB_NAME", "tirelire"),
)

engine = create_engine(database_url, future=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

Base = declarative_base()
