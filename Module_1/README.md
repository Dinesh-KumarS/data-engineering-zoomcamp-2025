## Module 1 Homework

## Docker & SQL

## Question 1. Understanding docker first run 

Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.

What's the version of `pip` in the image?

- 24.3.1
- 24.2.1
- 23.3.1
- 23.2.1

Answer: 24.3.1

<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_1.png" width="800" height="400"><br>

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

Answer: postgres:5432

# Postgres

## Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, **respectively**, happened:
1. Up to 1 mile
2. In between 1 (exclusive) and 3 miles (inclusive),
3. In between 3 (exclusive) and 7 miles (inclusive),
4. In between 7 (exclusive) and 10 miles (inclusive),
5. Over 10 miles 

Options:

- 104,802;  197,670;  110,612;  27,831;  35,281
- 104,802;  198,924;  109,603;  27,678;  35,189
- 104,793;  201,407;  110,612;  27,831;  35,281
- 104,793;  202,661;  109,603;  27,678;  35,189
- 104,838;  199,013;  109,645;  27,688;  35,202

Answer: 104,802;  198,924;  109,603;  27,678;  35,189

```SQL
WITH segmentation AS (
SELECT *
	, CASE 
		WHEN trip_distance <= 1.00 THEN 1
		ELSE 0
	END AS one_mile
	, CASE 
		WHEN trip_distance > 1.00 AND trip_distance <= 3.00 THEN 1
		ELSE 0
	END AS one_to_three_mile
	, CASE 
		WHEN trip_distance > 3.00 AND trip_distance <= 7.00 THEN 1
		ELSE 0
	END AS three_to_seven_mile
	, CASE 
		WHEN trip_distance > 7.00 AND trip_distance <= 10.00 THEN 1
		ELSE 0
	END AS seven_to_ten_mile
	, CASE 
		WHEN trip_distance > 10.00 THEN 1
		ELSE 0
	END AS ten_mile
FROM green_trip_data
WHERE CAST(lpep_dropoff_datetime AS DATE) >= '2019-10-01' AND CAST(lpep_dropoff_datetime AS DATE) <= '2019-10-31')

SELECT sum(one_mile) AS one_mile
	, sum(one_to_three_mile) AS one_to_three_mile
	, sum(three_to_seven_mile) AS three_to_seven_mile
	, sum(seven_to_ten_mile) AS seven_to_ten_mile
	, sum(ten_mile) AS ten_mile
FROM segmentation;
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_3.png" width="600" height="400">
<br>

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance. 

- 2019-10-11
- 2019-10-24
- 2019-10-26
- 2019-10-31

Answer: 2019-10-31

```SQL
SELECT 
	CAST(lpep_pickup_datetime AS DATE) AS DATE
	, MAX(trip_distance) AS max_trip_distance
FROM green_trip_data
GROUP BY CAST(lpep_pickup_datetime AS DATE)
ORDER BY max_trip_distance DESC;
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_4.png" width="600" height="400">
<br>

## Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in
`total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.
 
- East Harlem North, East Harlem South, Morningside Heights
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

Answer: East Harlem North, East Harlem South, Morningside Heights

```SQL
SELECT 
	CAST(GT.lpep_pickup_datetime AS DATE) AS lpep_pickup_datetime
	, ZL."Zone"
	, SUM(GT."total_amount") AS total_amount
FROM green_trip_data GT
INNER JOIN taxi_zone_lookup ZL
	ON GT."PULocationID" = ZL."LocationID"
WHERE CAST(lpep_pickup_datetime AS DATE) = '2019-10-18'
GROUP BY CAST(GT.lpep_pickup_datetime AS DATE)
	, ZL."Zone"
ORDER BY total_amount DESC;
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_5.png" width="600" height="400">
<br>

## Question 6. Largest tip

For the passengers picked up in October 2019 in the zone
name "East Harlem North" which was the drop off zone that had
the largest tip?

Note: it's `tip` , not `trip`

We need the name of the zone, not the ID.

- Yorkville West
- JFK Airport
- East Harlem North
- East Harlem South

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
	AND ZL."Zone" = 'East Harlem North'
LEFT JOIN taxi_zone_lookup TZL
	ON GT."DOLocationID" = TZL."LocationID"
WHERE CAST(lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-30'
ORDER BY GT.tip_amount DESC;
```
<br>
<img src="https://github.com/Dinesh-KumarS/data-engineering-zoomcamp-2025/blob/main/Module_1/Images/Question_6.png" width="800" height="400">
<br>

## Terraform

## Question 7. Terraform Workflow

Which of the following sequences, **respectively**, describes the workflow for: 
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform
   
Options:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm

Answer: terraform init, terraform apply -auto-approve, terraform destroy

