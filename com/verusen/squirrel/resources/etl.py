import psycopg2
import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from sqlalchemy.dialects.postgresql import insert as pg_insert
from com.verusen.squirrel.entities.Area import Area
from com.verusen.squirrel.entities.Park import Park
from com.verusen.squirrel.entities.Animal import Animal
from com.verusen.squirrel.entities.Squirrel import Squirrel
from com.verusen.squirrel.entities.Activity import Activity

def run_etl(engine):
    spark  = SparkSession.builder.appName('squirrelApp').getOrCreate()

    # Regular expresion that matches any characters enclosed in parentheses ()    
    pattern = r"\(.*?\)"

    # Reading CSV files
    df_park_init = spark.read.csv("./com/verusen/squirrel/data/park-data.csv", header=True, inferSchema=True)
    print(f"{datetime.datetime.now()} Park file read")
    df_squirrel_init = spark.read.csv("./com/verusen/squirrel/data/squirrel-data.csv", header=True, inferSchema=True)
    print(f"{datetime.datetime.now()} Squirrel file read")
    
    # Creating dataframe for areas
    df_area = df_park_init.select(["Area ID","Area Name"])
    df_area = df_area.withColumnsRenamed({"Area ID":"id","Area Name":"name"}).distinct().orderBy("Area ID")
    print(f"{datetime.datetime.now()} Area dataframe filtered")

    # Creating dataframe for parks
    df_park = df_park_init.select(["Park ID","Park Name","Area ID"])
    df_park = df_park.withColumnsRenamed({"Park ID":"id","Park Name":"name","Area ID":"area_id"}).distinct().orderBy("id")
    print(f"{datetime.datetime.now()} Park dataframe filtered")

    # Creating dataframe for animals
    df_animal = df_park_init.select(["Park ID","Other Animal Sightings"])
    df_animal = df_animal.withColumnsRenamed({"Park ID":"park_id","Other Animal Sightings":"description"}).distinct().orderBy("park_id")
    # Clean the words that are inside parentesis
    df_cleaned = df_animal.withColumn("description", F.regexp_replace(df_animal.description, pattern, ""))
    # Explode and split by te comma
    df_animal = df_cleaned.withColumn("description", F.explode(F.split(df_cleaned.description, ","))).dropna().orderBy("park_id")
    df_animal = df_animal.select("park_id", "description")
    df_animal = df_animal.withColumn("description",F.trim(F.col("description"))).distinct()    
    print(f"{datetime.datetime.now()} Animal dataframe filtered")

    # Creating squirrel dataframe
    df_squirrel = df_squirrel_init.select(["Squirrel ID","Park ID","Primary Fur Color"])
    df_squirrel = df_squirrel.withColumnsRenamed({"Squirrel ID":"id","Park ID":"park_id","Primary Fur Color":"primary_color"}).distinct().orderBy("id")    
    # Complete with Unknown when is null
    df_squirrel = df_squirrel.fillna("Unknown",subset=["primary_color"])    
    print(f"{datetime.datetime.now()} Squirrel dataframe filtered")    

    #Creation activities dataframe
    df_activity = df_squirrel_init.select(["Squirrel ID","Activities"])
    df_activity = df_activity.withColumnsRenamed({"Squirrel ID":"squirrel_id","Activities":"description"}).distinct().orderBy("squirrel_id")    
    # Clean the words that are inside parentesis
    df_cleaned = df_activity.withColumn("description",F.regexp_replace(df_activity.description, pattern, ""))
    # Complete with Unknown when is null
    df_activity = df_cleaned.fillna("Unknown", subset=["description"])    
    df_explode = df_activity.withColumn("description",F.explode(F.split(df_activity.description, ",")))    
    df_activity = df_explode.withColumn("description",F.trim(F.col("description")))    
    print(f"{datetime.datetime.now()} Activity dataframe filtered")

    #insert to sql
    insert_sql(df_area,['id'],engine, Area)
    insert_sql(df_park,['id'],engine, Park)
    insert_sql(df_animal,['park_id','description'], engine, Animal)
    insert_sql(df_squirrel,['id'],engine, Squirrel)
    insert_sql(df_activity,['squirrel_id','description'], engine, Activity)
    spark.stop()

def insert_sql(dataframe, constraint, engine, entity):
    df_panda = dataframe.toPandas()
    data_to_insert = df_panda.to_dict(orient='records') 
    insert_query = pg_insert(entity).values(data_to_insert)
    ignore_query = insert_query.on_conflict_do_nothing(index_elements = constraint)
    with engine.begin() as conn:
         result = conn.execute(ignore_query)
         print(f"{datetime.datetime.now()} Insert result:", result.rowcount)