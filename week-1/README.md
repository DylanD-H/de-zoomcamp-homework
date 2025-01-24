SQL for week 1 Homeowrk Questions

Question 3:	

SELECT
	CASE
		WHEN trip_distance <= 1 THEN 'Up to 1 mile'
		WHEN trip_distance > 1 AND trip_distance <=3 THEN 'Between 1 and 3 miles'
		WHEN trip_distance > 3 AND trip_distance <=7 THEN 'Between 3 and 7 miles'
		WHEN trip_distance > 7 AND trip_distance <=10 THEN 'Between 7 and 10 miles'
		ELSE 'Over 10 miles'
	END AS distance_ranges,
	COUNT(1) as trip_count

FROM green_taxi_data
WHERE
	lpep_pickup_datetime >= '2019-10-01' AND
	lpep_dropoff_datetime < '2019-11-01'

GROUP BY
	distance_ranges;



Question 4:

SELECT
	DATE(lpep_pickup_datetime) AS pickup_date,
	MAX(trip_distance) AS max_trip_distance
	
FROM green_taxi_data

WHERE 
	DATE(lpep_pickup_datetime) IN ('2019-10-11','2019-10-24','2019-10-26','2019-10-31')

GROUP BY pickup_date

ORDER BY max_trip_distance DESC;



Question 5:

SELECT
	SUM(total_amount) AS totals,
	zpu."Zone" AS pickup_location
	
	
FROM 
	green_taxi_data t JOIN zones zpu
	ON t."PULocationID" = zpu."LocationID"

WHERE
	DATE(t.lpep_pickup_datetime) = '2019-10-18'

GROUP BY pickup_location
HAVING 
	SUM(total_amount) > 13000

ORDER BY totals DESC;



Question 6:

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
