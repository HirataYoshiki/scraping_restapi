#データベース設計とその操作に関するファイル
import os
import sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


url = os.path.join(os.path.dirname(__file__),"test.db") 
DB_URL = f'sqlite:///{url}'

engine = sqlalchemy.create_engine(DB_URL, echo=True)
Session = sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = engine
    )
SessionLocal = Session()

Base = declarative_base()

class Activity(Base):
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer)
    timestamp = Column(DateTime)
    action = Column(String)
    items = Column(String)
    __tablename__ = "activities"

class User(Base):
    userid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    premium = Column(Boolean,default = False)
    __tablename__ = "users"


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    
        