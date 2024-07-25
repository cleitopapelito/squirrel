from sqlalchemy import Column, String, Integer, UniqueConstraint
from com.verusen.squirrel.entities.Base import Base

class Activity(Base):
    __tablename__= "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    squirrel_id = Column(String(50))
    description = Column(String(250))

    __table_args__= (UniqueConstraint('squirrel_id', 'description', name='unique_squirrel_activities'),)