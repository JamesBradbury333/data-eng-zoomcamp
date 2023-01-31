# Here we are modifying the ingest_script.py from week-1 and refactor it
# so that it is more of an ETL. Using prefecture decorators allows us to
# run the script using sheduling and keep track of jobs using a GUI.
# (similar to airflow and other such tools)

import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
import psycopg2
import os

# TODO: Set up a logger
# TODO: Look at reading in data in chunks but in a better way than week-1   
@flow(name="Ingest Data")
def main():
    user = "postgres"
    password = "password"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"
    table_name = "yellow_taxi_trips-week2"
    csv_path = "week-1/python_docker_sql/database/yellow_tripdata_2021-01.csv"
    print(os.getcwd())

    db_engine_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    db_engine = create_engine(db_engine_url)
    data = extract_data(csv_path)
    transformed_data = transform_data(data)
    load_data(db_engine, table_name, transformed_data)
    print("ETL job completed successfully!")


@task(name="Extract-Taxi-Data", log_prints=True, retries=3)
def extract_data(csv_path):
    print(f"Loading file: {csv_path}")
    df = pd.read_csv(csv_path)
    return df

@task(name="Transform-Taxi-Data", log_prints=True, retries=3)
def transform_data(df: pd.DataFrame):
    print("Converting datetime columns to datetime types")
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    return df

@task(name="Load-Taxi-Data", log_prints=True, retries=3)
def load_data(db_engine, db_tablename: str, df: pd.DataFrame):
    print("Loading data into db...")
    df.to_sql(name=db_tablename, con=db_engine, if_exists="replace")
    print("Data loaded into db")


if __name__ == "__main__":
    main()
