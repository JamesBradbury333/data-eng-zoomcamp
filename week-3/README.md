# Data Warehousing
## OLTP vs OLAP
Online Transactional Processing vs Online Analytics Processing. OLTP is a upto date database containing the most accurate data, exaples such as customer order tables, product info etc and must be accurate. OLAP is for conducting large scale analytics, often used by Business Analysts and other technical people. OLPA are updated periodically in large batches, often scale of Big Data.
## BigQuery
Big Query is Google's out of the box tool for creating a Data Warehouse. No need to provision or manage infrastructure and can easily be scaled. Not really a Database software but is interacted with in the same way.
## Optimising BigQuery
We can make optimisations on tables to help queries run faster. Indexing is the classic way for joins and clause queries but if we find a particular table is being searched for with similar clauses on a particular column Partioning and Clusteing can also be helpful.
### Partions
You can partition tables in Big Query to break a table into sections by the most often 'claused' columns. For instance if queries are often sent looking for data between 2 date ranges you can partion the table by Month or Year and a smaller subsection of the tables will need to be searched.
### Indexing
Prevents the need for sequential scans (searching through every row in a table sequentially). Basically a hashtable where the initial search key is a most commonly accessed column of data. For instance the primary key of a table will likely be used often in joining on other tables. The Search Key has a pointer to where the data can be found in memory allowing that data to be retrieved more easily. Adding indexing increases the size of the table and the level of maintainence it requires (adding indexes is not cost free).
## BigQuery Best Practices
### Cost Reduction
* Avoid SELECT *
* Price Queries before running
* Use clustered, partitioned or indexed tables
* Use streaming inserts with caution
* Materialize query results in stages
### Query Performance
* Filter on paritioned tables
* Denormalize data
* Use nested or repeated columns
* Use external data sources appropriately (not too much/often)
* Reduce data before using a join
* Do not treat WITH clauses as prepared statements
* Avoid oversharing tables
* Avoid JavaScript user-defined functions
* Use approx aggregation functions (HyperLogLog++)
* Order Last for Query Operations to maximise performance
* Optimixe Joins
* Table with largest number of rows first, then table with fewest rows and then remaining tables decreasing by size.
