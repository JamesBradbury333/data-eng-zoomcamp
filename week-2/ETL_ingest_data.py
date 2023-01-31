# Here we are modifying the ingest_script.py from week-1 and refactor it
# so that it is more of an ETL. Using prefecture decorators allows us to
# run the script using sheduling and keep track of jobs using a GUI.
# (similar to airflow and other such tools)

import pandas as pd
from prefect import flow, task


@flow(name="Ingest Data")
def main():
    user = "postgres"
    password = "password"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"
    table_name = "yellow_taxi_trips"
    csv_path = "../week-1/database/yellow_tripdata_2021-01.csv"

    extract_data(csv_path)


@task(name="Extract-Taxi-Data", log_prints=True, retries=3)
def extract_data(csv_path):
    df = pd.read_csv(csv_path)
    pass


def transform_data():
    pass


def load_data():
    pass


if __name__ == "__main__":
    main()
