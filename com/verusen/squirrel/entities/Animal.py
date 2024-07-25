from sqlalchemy import Column, String, Integer, Float, UniqueConstraint
from com.verusen.squirrel.entities.Base import Base

class Animal(Base):
    __tablename__= "animals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    park_id = Column(Float)
    description = Column(String(250))

    __table_args__ = (UniqueConstraint('park_id', 'description', name='unique_park_animal'),)