from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(colour: str, year: int, month: int) -> Path:
    """Downoad trip data from GCS Bucket."""
    gcs_path = f"week-2/data/{colour}/{colour}_tripdata_{year}-{month:02}.parquet"
    print(f"gcs_path: {gcs_path}")
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task()
def transform(path: Path) -> pd.DataFrame:
    """Take a .parquet Path object and returns a cleaned (kinda) pd.DataFrame."""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df["passenger_count"].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery."""
    # TODO: Credentials not working, read over notes and fix in prefect
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-credentials")

    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="data-eng-course-375719",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query."""
    colour = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(colour, year, month)
    print(f"path returned: {path}")
    df = transform(path)
    write_bq(df)


if __name__ == "__main__":
    etl_gcs_to_bq()
