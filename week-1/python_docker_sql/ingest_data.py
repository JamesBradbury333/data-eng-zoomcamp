import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import logging

##################################
## Run using:
##  python ingest_data.py postgres password localhost 5432 ny_taxi yellow_taxi_data database/yellow_tripdata_2021-01.csv 
## Think about creating a config file to set these environment variables
##################################


def main(params):
    DB_UPLOAD_CHUNKSIZE = 50000
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info(f"running {__name__}")
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.db
    table_name = params.table_name
    csv_name = params.csv_path


    # import the csv
    # could potentially download each time but no need
    df = pd.read_csv(csv_name, nrows=100)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
    
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    logging.info(f"postgresql://{user}:{password}@{host}:{port}/{database}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=DB_UPLOAD_CHUNKSIZE)
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    logging.info("Added first row of data to db")
    logging.info(df.head(n=0))

    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists="append")
        t_end = time()
        logging.info("inserted another chunk to db...")
        logging.info(f"insertion took {t_end - t_start}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data ot Postgres")
    parser.add_argument("user", help="user name for postgres")
    parser.add_argument("password", help="pasword for postgres user")
    parser.add_argument("host", help="host for postgres")
    parser.add_argument("port", help="port for postgres")
    parser.add_argument("db", help="postgres database name")
    parser.add_argument(
        "table_name", help="table name for the data to be uploaded into"
    )
    parser.add_argument(
        "csv_path", help="csv_path of the file to be uploaded to postgres"
    )
    args = parser.parse_args()
    main(args)
