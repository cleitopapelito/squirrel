from sqlalchemy import func,select, desc
from com.verusen.squirrel.entities.Area import Area
from com.verusen.squirrel.entities.Park import Park
from com.verusen.squirrel.entities.Animal import Animal
from com.verusen.squirrel.entities.Squirrel import Squirrel
from com.verusen.squirrel.entities.Activity import Activity

def sql_questions(session):
    # How may squirrels are in each park
    query = (
        select(
            Park.id, Park.name,
            func.count(Squirrel.park_id).label("squirrel_count")
        )
        .select_from(Park)
        .join(Squirrel, Park.id == Squirrel.park_id)
        .group_by(Park.id, Park.name)
        .order_by(Park.id)
    )
    
   
    result = session.execute(query)
    print("--> How many squirrels are there in each Park?")
    for id, park_name, squirrel_count in result:
        print(f"Squirrel count [{squirrel_count}] Park: {id} - {park_name}")

    # #How many squirrels are there in each Borough 
    query = (
        select(
            Area.id, Area.name,
            func.count(Squirrel.park_id).label("squirrel_count")
        )
        .select_from(Park)
        .join(Squirrel, Park.id == Squirrel.park_id)
        .join(Area, Area.id == Park.area_id)
        .group_by(Area.id, Area.name)
        .order_by(Area.id)
    )

    result = session.execute(query)
    print("--> How many squirrels are there in each Borough?")
    for id, area_name, squirrel_count in result:
        print(f"Squirrel count: [{squirrel_count}] Borough: {id} - {area_name}")

    #A count of "Other Animal Sightings" by Park
    query = (
        select(
            Park.id, Park.name,
            Animal.description,
            func.count(Animal.park_id).label("animal_count")
        )
        .select_from(Park)
        .join(Animal, Park.id == Animal.park_id)
        .group_by(Park.id, Park.name, Animal.description)
        .order_by(Park.id)
    )

    result = session.execute(query)
    print("--> A count of Other Animal Sightings by Park")

    for id, park_name, description, animal_count in result:
        print(f"Park: {id} - {park_name}, Animal: {description} [{animal_count}]")

    # What is the most common activity for Squirrels
    subquery = (
        select(
            Activity.description,
            func.count(Activity.squirrel_id).label("squirrel_count"),
            func.rank().over(order_by=func.count(Activity.squirrel_id).desc()).label("rank")
        )
        .select_from(Activity)
        .group_by(Activity.description)
        .subquery()
    )    

    query = (
        select(subquery.c.description)
        .where(subquery.c.rank == 1)
    )
    result = session.execute(query).scalar()

    print("--> The most common activity for squirrels is", result)

    # A count of all Primary Fur Colors by Park
    query=(
        select(
            Park.id, Park.name,
            Squirrel.primary_color,
            func.count(Squirrel.park_id).label("squirrel_count")
        )
        .select_from(Park)
        .join(Squirrel, Park.id == Squirrel.park_id)
        .group_by(Park.id, Park.name, Squirrel.primary_color)
        .order_by(Park.id)
    )
    result = session.execute(query)
    print("--> A count of all Primary Fur Colors by Park")
    for id, park_name,squirrer_primary_color, squirrel_count in result:
        print(f"Park: {id} - {park_name}, Primary fur color: {squirrer_primary_color}, count [{squirrel_count}]")