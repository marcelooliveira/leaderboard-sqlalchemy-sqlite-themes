from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()

class Score(Base):
    __tablename__ = 'scores'
    id = Column(String, primary_key=True)  # Using String instead of UUID
    avatar = Column(Integer)
    playername = Column(String)
    points = Column(Integer)
