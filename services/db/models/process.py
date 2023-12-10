from sqlalchemy import Column, Integer, String

from ..db import TimedModel

class Process(TimedModel):
    __tablename__ = 'processes'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    group = Column(String)
    