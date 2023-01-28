-- Postgres SQL queries for obtaining the answers

-- Question 3: how many trips on Jan 15
SELECT COUNT(*) FROM green_taxi_data
	WHERE lpep_pickup_datetime >= '2019-01-15 00:00:00'
		AND lpep_pickup_datetime <= '2019-01-15 23:59:59'
	AND lpep_dropoff_datetime >= '2019-01-15 00:00:00'
		AND lpep_dropoff_datetime <= '2019-01-15 23:59:59';



-- Question 4: Largest trip for each day
SELECT lpep_pickup_datetime, lpep_dropoff_datetime FROM green_taxi_data 
WHERE trip_distance = (SELECT MAX(trip_distance) FROM green_taxi_data)



-- Question 5. The number of passengers
SELECT COUNT(*) FROM green_taxi_data 
WHERE lpep_pickup_datetime >= '2019-01-01 00:00:00'
		AND lpep_pickup_datetime <= '2019-01-01 23:59:59'
AND passenger_count = 2;

SELECT COUNT(*) FROM green_taxi_data 
WHERE lpep_pickup_datetime >= '2019-01-01 00:00:00'
		AND lpep_pickup_datetime <= '2019-01-01 23:59:59'
AND passenger_count = 3;



-- Question 6 Largest tip
-- Answer is largest_tip_do_zone col in final result
CREATE TEMP TABLE  pickup_astoria AS
SELECT gtd.* FROM green_taxi_data gtd
	INNER JOIN taxi_zone_lookup tzl
	ON gtd."PULocationID" = tzl."LocationID"
	WHERE tzl."Zone" = 'Astoria';
	
SELECT pa.*, tzl."Zone" as largest_tip_do_zone FROM pickup_astoria pa
	INNER JOIN taxi_zone_lookup tzl
	ON pa."DOLocationID" = tzl."LocationID"
		WHERE tip_amount = (SELECT MAX(tip_amount) FROM pickup_astoria);
	