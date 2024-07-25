from sqlalchemy import Column, String, Float
from com.verusen.squirrel.entities.Base import Base

class Park(Base):
    __tablename__ = "parks"

    id = Column(Float, primary_key= True)
    name = Column(String(250))
    area_id = Column(String(50))