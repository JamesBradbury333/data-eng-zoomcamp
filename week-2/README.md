# Week 2

## Ingest Data into db
Spin up docker database from week-1 then: 
``` -- Fenced Code Block here
$python week-2/ETL_ingest_data.py
```
to ingest yellow_taxi_data into warehouse using prefecture ETL.


## Manage Flows in Prefect Orion
Inside the environment you have installed prefect (python package) run:
```
$prefect orion start
```
This launches dashboard server you can access through the browser to manage the flows within  the ETL_ingest_data.py script