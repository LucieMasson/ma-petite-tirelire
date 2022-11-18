import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Session, declarative_base, scoped_session, sessionmaker


engine = create_engine(
        "postgresql://{}:{}@{}:{}/{}".format(
            os.environ.get('DB_USER', 'test_user'),
            os.environ.get('DB_PASSWORD', 'test'),
            os.environ.get('DB_HOST', 'localhost'),
            os.environ.get('DB_PORT', '5437'),
            os.environ.get('DB_NAME', 'tirelire'),
        )
    )


session = scoped_session(sessionmaker())
session.configure(bind=engine)


def test_tf_haha():
    assert True
