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
## Prefect Orion GCP Credentials Block
Go into Prefect Dashboard and Create a GCP block there (requires the pip/conda installation of "prefect_gcp[cloud_storage]" --> in requirements.txt). For a given IAM role in the console you can download a .json key and paste it into Prefect Orion to create the Block. Prefect Orion provides python code for accessing the credentials from the script.


## Load Data from web host into GCP Bucket.
```bash
$ python week-2/gcp/etl_web_to_gcs.py 
```
This loads yellow_taxi .csv data from a url hosted by DataTalksClub into a GCP bucket.
Data is saved locally as .parquet and is then uploaded to the GCP bucket with the same file path but in the cloud rather than locally. 
* GCP Credentials named "zoom-gcp-credentials" have been created in GCP console and have been added as a Block in Prefect Orion. Prefect Orion dashboard server must be up so that the credentials can be read in. 

## Load Data From GCP Bucket into BigQuery (GoogleSQL) table.
<mark> make sure the project_id is correct --> I spent ages in IAM premissions docs when infact I was trying to upload data to someone elses project </mark>  

``` bash
$ python week-2/gcp/etl_gcs_to_bq.py
```
* Uses GCP Credentials named "zoom-gcp-credentials" stored in Prefect Orion.
* Needs a to be a role with "BigQuery Admin" and "Storage Admin" permisions.
* Needs "ride" BigQuery table already created.

## Building a Flow to run on a schedule.
Requires a script.
``` bash
$ prefect deployment build flow week-2/gcp/parameterized_flow.py
```
This builds a .yaml file in the root with a recipe for running a flow at regular intervals. Cron schedules etc can be added. Works by cloning everything below working directory so data-volumes with permssion restircitions can cause issues. There is a .prefectignore file which can help with this. You can specify which parameters you want to run the flow with or just run with default.

After updating the .yaml you can update the flow using
``` bash
$ prefect deployment apply etl_parent_flow-deployment.yaml
```

You can monitor the progress of a flow run in the CLI using the prefect agent
``` bash
$ prefect agent start --work-queue "default"
```
This show you the progress of the work queue "default". You can create other work queues and attach flows to them.

## Building a Flow using a DockerContainer
Need to set prefcet congfig api_address so docker container can interact with prefect orion server
``` bash
$ prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
```

Create a DockerFile containing parameterized_flow.py script and Build it:
``` bash
$ docker image build -t docker-username/prefect:de-zoom .
```
Publish the image to your docker hub:
``` bash
$ docker image push  jamesbradbury222/prefect:de-zoom .
```
Now you can go into Prefect Orion Deployments and set up a Docker Deployment.
Running the script docker_deploy.py creates the new deployment:
``` bash
$ python docker_deploy.py
``` 
