from sqlalchemy import Column, Integer, Date, String, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True)
    username = Column(String)

class Excercise(Base):
    __tablename__ = "excercises"

    exid = Column(Integer, primary_key=True)
    uid = Column(ForeignKey("users.uid"))
    description = Column(String, nullable=False)
    duration = Column(Integer, default=0)
    date = Column(Date, nullable=False)
