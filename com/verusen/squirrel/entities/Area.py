from sqlalchemy import Column, String
from com.verusen.squirrel.entities.Base import Base

class Area(Base):
    __tablename__ = "areas"

    id = Column(String(50), primary_key=True)
    name = Column(String(255))  