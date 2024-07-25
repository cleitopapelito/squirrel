from com.verusen.squirrel.resources.etl import run_etl
from com.verusen.squirrel.services.dbEngine import db_engine
from com.verusen.squirrel.resources.questions import sql_questions
import datetime

if __name__ == '__main__':
    print(f"{datetime.datetime.now()} Starting squirrel app")
    engine, session = db_engine()
    run_etl(engine)
    sql_questions(session)
    session.close()
    engine.dispose()
    print(f"{datetime.datetime.now()} Ending squirrel app")