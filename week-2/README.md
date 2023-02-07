# Week 2

## Ingest Data into db

### <mark>This script is broken atm. Prefect docs provide code to use a context manager when creating a db_connection. Error is arising with saying 'asynch' context manager must be used instead. Problem with prefect not the script I think.</mark>
## 
Spin up docker database from week-1 then: 
```bash
$ python week-2/ETL_ingest_data.py
```
to ingest yellow_taxi_data into warehouse using prefecture ETL.


## Manage Flows in Prefect Orion
Inside the environment you have installed prefect (python package) run:
```bash
$ prefect orion start
```
This launches dashboard server you can access through the browser to manage the flows within  the ETL_ingest_data.py script

## Manage db connection with Prefect Orion
Perfect Orion can manage connections to services for us. See [prefect collections catalog](https://docs.prefect.io/collections/catalog/).
As we have prefect-sqlalchemy installed we can use prefect to setup and manage db connections rather than using psychopg2 and parameters/environment variables.

After creating a conneciton in the prefect orion dashboard server, the sever provides us with code such as the following to connect to our db:
```python
from prefect_sqlalchemy import SqlAlchemyConnector

with SqlAlchemyConnector.load("postgres-ny-taxi-connector") as database_block:

```

## Load Data into GCP Bucket.
```bash
$ python week-2/gcp/etl_web_to_gcs.py 
```
This loads yellow_taxi .csv data from a url hosted by DataTalksClub into a GCP bucket.
Data is saved locally as .parquet and is then uploaded to the GCP bucket with the same file path but in the cloud rather than locally. 
* GCP Credentials named "zoom-gcp-credentials" have been created in GCP console and have been added as a Block in Prefect Orion. Prefect Orion dashboard server must be up so that the credentials can be read in. 