from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3, log_prints="True")
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
    """Write DataFrame as a parquet file"""
    df.to_parquet(localpath, compression="gzip")
    return

@task()
def write_gcs(from_path: Path, to_path: str) -> None:
    """Uploading local parquet file to google cloud storage"""
    gcp_block = GcsBucket.load("zoom-gcs")
    gcp_block.upload_from_path(
        from_path=from_path, to_path=to_path
    )
    return


@flow(log_prints="True")
def etl_web_to_gs() -> None:
    """The main ETL function."""
    colour = "yellow"
    year = 2021
    month = 1
    dataset_file = f"{colour}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{colour}/{dataset_file}.csv.gz"
    local_parquet_path = Path(f"week-2/data/{colour}/{dataset_file}.parquet")
    cloud_path = local_parquet_path

    df = fetch(dataset_url)
    df_clean = clean(df)
    write_local(df_clean, local_parquet_path)
    write_gcs(from_path=local_parquet_path, to_path=cloud_path)


if __name__ == "__main__":
    etl_web_to_gs()
