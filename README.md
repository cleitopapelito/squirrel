# SQUIRREL APP
Squirrel App is a project that extract information from [The Squirrel Census](https://www.thesquirrelcensus.com/) and allows you to explore interesting facts about squirrel activity and distribution.

## Pre requisites
Docker (this project was created with Docker version 27.0.3) https://docs.docker.com/get-docker/

### Configure your environment
1. Rename the 'env_template' file to '.env.'

2. Inside the '.env' file, configure the following parameters to specify where the services of the Squirrel App and the database will be allocated:
DB_NAME=squirrel_db
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432
SQUIRREL_PORT=8080

### Running the application
1. In the project folder execute:
docker compose up --build

- The first time this is executed, the database will be created.
- On subsequent executions, the data will be persisted and transformed.
#### Data Verification

1. Connect to the Docker container via terminal (replace 'squirrel-postgres-1' with the name of the PostgreSQL container):
docker exec -it squirrel-postgres-1 bash

2. Switch to the database user:
su postgres

3.  Open PostgreSQL
psql

4.  Connect to the database. Replace 'squirrel_db' with the database name configured in your .env file:
\c squirrel_db

5. Describe the objects created in the database:
\d

6. Describe a especific object, for example the areas table:
\d areas

7. Retrieve and display the data:
select * from areas;