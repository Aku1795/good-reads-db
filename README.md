# good-reads-db

In this project, I will be creating a database for the Goodreads dataset. 
The dataset is available on Kaggle and can be found [here](https://www.kaggle.com/jealousleopard/goodreadsbooks).

## Postgres Database

The database consists of one table called `books`. Its schema can be found in the `model.py` file. It is currently hosted
on Aiven.

## Database migration

In case of schema changes, database migration can be performed using alembic. To do so:

- cd into the app directory
- modify the schema in the `model.py` file
- if needed modify the etl process to reflect the schema changes
- run `alembic revision -m "migration message"`
- run `alembic upgrade head`

Please note that this process is done locally. You need therefore to have alembic and sqlalchemy installed on your local
machine. Also please make sure to have the database connection string in the `.env` file in the root directory of the project
and export the variables present in it to your terminal session.

## ETL

The ETL process is done in the `etl.py` file. The process is as follows:

1. Load the data from the CSV file.
2. Clean the data.
3. Insert data into the `books` table.

### Running the ETL process

Before running the ETL process, make sure you have the following in place:

- A csv file named `books.csv` containing books data in the `dataset` directory which will be mounted to the 
docker container as a volume.
- An .env file containing the database connection string. The string should be stored inside `DB_URI` variable and the 
.env file should be in the root directory of the project.

Once the above is in place, run the following command to start the ETL process`docker compose up`

This will start the ETL process and insert the data into the database.

Once the process is done, you can run `docker compose down` to stop the process.

