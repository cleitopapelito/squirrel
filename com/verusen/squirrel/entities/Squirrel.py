from sqlalchemy import Column, String, Float
from com.verusen.squirrel.entities.Base import Base

class Squirrel(Base):
    __tablename__= "squirrels"

    id = Column(String(50), primary_key=True)
    park_id = Column(Float)
    primary_color = Column(String(250))