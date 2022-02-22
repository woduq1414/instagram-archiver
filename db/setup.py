from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from db.models import *

from sqlalchemy.orm import sessionmaker, scoped_session

from config import DB_URL


engine = create_engine(DB_URL, echo=True)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = Session()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# def init():
#     InstaUser.__table__.create(bind=engine, checkfirst=True)
#     PostData.__table__.create(bind=engine, checkfirst=True)
#     MediaSrc.__table__.create(bind=engine, checkfirst=True)

if __name__ == "__main__":
    pass
    # init()