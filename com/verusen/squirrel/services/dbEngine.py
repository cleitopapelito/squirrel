from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
#from com.verusen.squirrel.entities.entities import *
from com.verusen.squirrel.entities.Base import Base

def db_engine():
    
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USERNAME')
    DB_PASS = os.environ.get('DB_PASSWORD')
    DB_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine = create_engine(DB_URI)

    # Create all tables defined based on our classes (entities)
    Base.metadata.create_all(engine)

    # Create a session object for interacting with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session
