## Module 1 Homework

## Docker & SQL

## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

Answer: --rm

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0
- 1.0.0
- 23.0.1
- 58.1.0

Answer: 0.45.1 (pip wheel version got updated)
```
docker run -it --entrypoint=bash python:3.9
pip list
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_2.png" width="800" height="400"><br>

# Postgres

## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- 15612
- 15859
- 89009

Answer: 15612

```SQL
SELECT COUNT(*)
FROM green_trip_data
WHERE CAST(lpep_pickup_datetime AS DATE) = '2019-09-18'
AND CAST(lpep_dropoff_datetime AS DATE) = '2019-09-18';
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_3.png" width="600" height="400">
<br>

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every trip on a single day, we only care about the trip with the longest distance. 

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21

Answer: 2019-09-26

```SQL
SELECT "VendorID"
	, lpep_pickup_datetime
	, lpep_dropoff_datetime
	, (CAST(lpep_dropoff_datetime as TIME)-CAST(lpep_pickup_datetime as TIME)) AS TRIP_TIME
FROM green_trip_data
WHERE CAST(lpep_pickup_datetime AS DATE) = CAST(lpep_dropoff_datetime AS DATE)
ORDER BY TRIP_TIME DESC;
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_4.png" width="600" height="400">
<br>

## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

Answer: "Brooklyn" "Manhattan" "Queens”

```SQL
SELECT 
	"Borough"
	, sum(GT.total_amount)
FROM green_trip_data GT
INNER JOIN taxi_zone_lookup ZL
	ON GT."PULocationID" = ZL."LocationID"
	AND ZL."Borough" != 'Unknown'
WHERE CAST(lpep_pickup_datetime AS DATE) = '2019-09-18'
GROUP BY "Borough"
ORDER BY SUM DESC;
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_5.png" width="600" height="400">
<br>

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

Answer: JFK Airport

```SQL
SELECT
	GT."VendorID"
	, GT.lpep_pickup_datetime
	, GT.lpep_dropoff_datetime
	, GT."PULocationID"
	, GT."DOLocationID"
	, GT.tip_amount
	, ZL."LocationID"
	, ZL."Borough" AS pick_up_borough
	, ZL."Zone" AS pick_up_zone
	, TZL."Borough" AS drop_off_borough
	, TZL."Zone" AS drop_up_zone
FROM green_trip_data GT
INNER JOIN taxi_zone_lookup ZL
	ON GT."PULocationID" = ZL."LocationID"
	AND ZL."Zone" = 'Astoria'
LEFT JOIN taxi_zone_lookup TZL
	ON GT."DOLocationID" = TZL."LocationID"
WHERE CAST(lpep_pickup_datetime AS DATE) BETWEEN '2019-09-01' AND '2019-09-30'
ORDER BY GT.tip_amount DESC;
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_6.png" width="800" height="400">
<br>

## Terraform

## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_7.png" width="800" height="400">
<br>
