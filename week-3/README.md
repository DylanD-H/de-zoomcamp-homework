# Week 3 Homework
## Setup: 
### Create External & Materialized Tables
```SQL
CREATE OR REPLACE EXTERNAL TABLE nytaxi.external_yellow_tripdata
OPTIONS (
  format = 'parquet',
  uris = ['gs://bucket-name/*.parquet']
);
```
```SQL
CREATE OR REPLACE TABLE nytaxi.yellow_tripdata AS
SELECT * FROM nytaxi.external_yellow_tripdata;
```

## Question 1: 
What is count of records for the 2024 Yellow Taxi Data?

```SQL
SELECT COUNT(1) AS Row_Count
FROM `nytaxi.yellow_tripdata`;
```
| Row_Count |
|-----------|
| 20332093  |

## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.</br> 
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

```SQL
SELECT Count(DISTINCT PULocationID)
FROM `nytaxi.external_yellow_tripdata`;
```
**Estimate:** *0 B*
```SQL
SELECT Count(DISTINCT PULocationID)
FROM `nytaxi.yellow_tripdata`;
```
**Estimate:** *155.12 MB*

## Question 3:
Write a query to retrieve the PULocationID from the table in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

```SQL
SELECT PULocationID
FROM `nytaxi.yellow_tripdata`;
```
**Estimate:** *155.12 MB*
```SQL
SELECT PULocationID, DOLocationID
FROM `nytaxi.yellow_tripdata`;
```
**Estimate:** *310.24 MB*

*BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires 
reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.*

## Question 4:
How many records have a fare_amount of 0?
```SQL
SELECT COUNT(1) AS Row_Count
FROM `nytaxi.yellow_tripdata`
WHERE fare_amount = 0;
```
| Row_Count |
|-----------|
| 8333      |

## Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID

*Partition by tpep_dropoff_datetime and Cluster on VendorID*
```SQL
CREATE OR REPLACE TABLE `nytaxi.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime) 
CLUSTER BY VendorID AS
SELECT * FROM `nytaxi.external_yellow_tripdata`;
```
## Question 6:
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

```SQL
SELECT DISTINCT VendorID
FROM `nytaxi.yellow_tripdata`
WHERE DATE(tpep_dropoff_datetime) >= '2024-03-01' AND DATE(tpep_dropoff_datetime) <= '2024-03-15';
```
**Estimate:** *310.24 MB*

```SQL
SELECT DISTINCT VendorID
FROM `nytaxi.yellow_tripdata_partitioned_clustered`
WHERE DATE(tpep_dropoff_datetime) >= '2024-03-01' AND DATE(tpep_dropoff_datetime) <= '2024-03-15';
```
**Estimate:** *26.84 MB*
