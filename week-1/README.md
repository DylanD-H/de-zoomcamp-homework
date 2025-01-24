# Week 1 Homework
## Question 1. Understanding docker first run 
```bash
$ docker run -it --entrypoint=bash python:3.12.8
pip --version

pip 24.3.1
```
## Question 2. Understanding Docker networking and docker-compose

postgres service name: db  
postgres internal port: 5432

***db:5432***

## Question 3. Trip Segmentation Count
```SQL
SELECT
	CASE
		WHEN trip_distance <= 1 THEN 'Up to 1 mile'
		WHEN trip_distance > 1 AND trip_distance <= 3 THEN 'Between 1 and 3 miles'
		WHEN trip_distance > 3 AND trip_distance <= 7 THEN 'Between 3 and 7 miles'
		WHEN trip_distance > 7 AND trip_distance <= 10 THEN 'Between 7 and 10 miles'
		ELSE 'Over 10 miles'
	END AS distance_ranges,
	COUNT(1) as trip_count

FROM green_taxi_data
WHERE
	lpep_pickup_datetime >= '2019-10-01' AND
	lpep_dropoff_datetime < '2019-11-01'

GROUP BY
	distance_ranges;
```

| distance_ranges        | trip_count |
|------------------------|------------|
| Up to 1 mile           | 104802     |
| Between 1 and 3 miles  | 198924     |
| Between 3 and 7 miles  | 109603     |
| Between 7 and 10 miles | 27678      |
| Over 10 miles          | 35189      |



## Question 4. Longest trip for each day
```SQL
SELECT
	DATE(lpep_pickup_datetime) AS pickup_date,
	MAX(trip_distance) AS max_trip_distance
	
FROM green_taxi_data

WHERE 
	DATE(lpep_pickup_datetime) IN ('2019-10-11','2019-10-24','2019-10-26','2019-10-31')

GROUP BY pickup_date

ORDER BY max_trip_distance DESC;
```

| pickup_date | max_trip_distance |
|-------------|-------------------|
| 2019-10-31  | 515.89            |
| 2019-10-11  | 95.78             |
| 2019-10-26  | 91.56             |
| 2019-10-24  | 90.75             |



## Question 5. Three biggest pickup zones
```SQL
SELECT
	zpu."Zone" AS pickup_location,
	ROUND(CAST(SUM(total_amount) AS numeric),2) AS totals	
	
FROM 
	green_taxi_data t JOIN zones zpu
	ON t."PULocationID" = zpu."LocationID"

WHERE
	DATE(t.lpep_pickup_datetime) = '2019-10-18'

GROUP BY pickup_location
HAVING 
	SUM(total_amount) > 13000

ORDER BY totals DESC;
```

| pickup_location     | totals   |
|---------------------|----------|
| East Harlem North   | 18686.68 |
| East Harlem South   | 16797.26 |
| Morningside Heights | 13029.79 |



## Question 6. Largest tip
```SQL
SELECT
	MAX(Tip_amount) AS max_tip,
	zdo."Zone" AS dropoff_zone	
	
FROM 
	green_taxi_data t JOIN zones zpu
	ON t."PULocationID" = zpu."LocationID"
	JOIN zones zdo 
	ON t."DOLocationID" = zdo."LocationID"

WHERE
	zpu."Zone" = 'East Harlem North'

GROUP BY dropoff_zone
ORDER BY max_tip DESC
LIMIT 1;
```

| dropoff_zone | max_tip |
|--------------|---------|
| JFK Airport  | 87.3    |

## Question 7. Terraform Workflow
terraform init, terraform apply -auto-approve, terraform destroy
