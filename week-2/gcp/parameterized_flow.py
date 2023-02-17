# Parameterized version of etl_web_to_gcs.py script
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta


# TODO: Add seciton in the README.md ???
# TODO: This fails when kicking off a run using the .ymal in a Prefect Orion.
# This is because the postgres db-volume in week-1 is permission protected and prefecct oriion is trying to pull it
@task(retries=3, log_prints="True", cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read Taxi data from web into pandas DataFrame."""
    print(f"Reading dataset: {dataset_url}")

    df = pd.read_csv(dataset_url)
    return df


@task(log_prints="True")
def clean(df=pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues."""
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_drop_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"Rows: {len(df)}")
    return df


@task(log_prints="True")
def write_local(df: pd.DataFrame, localpath: Path) -> None:
    """Write DataFrame as a parquet file."""
    df.to_parquet(localpath, compression="gzip")
    return


@task()
def write_gcs(from_path: Path, to_path: str) -> None:
    """Uploading local parquet file to google cloud storage."""
    gcp_block = GcsBucket.load("zoom-gcs")
    gcp_block.upload_from_path(from_path=from_path, to_path=to_path)
    return


@flow(log_prints="True")
# FYI I would refactor this so that dataset_url and cloud_path were
# passed in as params but we're following the instructor.
def etl_web_to_gs(year: int, month: int, colour: str) -> None:
    """ETL Function loads data from repo into GCS bucket."""
    dataset_file = f"{colour}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{colour}/{dataset_file}.csv.gz"
    local_parquet_path = Path(f"week-2/data/{colour}/{dataset_file}.parquet")
    cloud_path = local_parquet_path

    df = fetch(dataset_url)
    df_clean = clean(df)
    write_local(df_clean, local_parquet_path)
    write_gcs(from_path=local_parquet_path, to_path=cloud_path)


# Parent flow for etl_web_to_gcs()
@flow()
def etl_parent_flow(
    months: list[int] = [1, 2], year: int = 2021, colour: str = "yellow"
): #TODO:Add docstring

    for month in months:
        etl_web_to_gs(year, month, colour)


if __name__ == "__main__":
    colour = "yellow"
    months = [1,2,3]
    year = 2021
    etl_parent_flow(months, year, colour)
