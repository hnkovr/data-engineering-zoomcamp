-- Solution for Qs.3-6 https://docs.google.com/forms/d/e/1FAIpQLSfZSkhUFQOf8Novq0aWTVY9LC0bJ1zlFOKiC-aVLwM-8LdxSg/viewform?pli=1

-- Question 3: Count records  (Multiple choice)
-- How many taxi trips were totally made on January 15?
-- *
-- 20689
-- 20530 +
-- 17630
-- 21090
SELECT COUNT(*)
FROM
    green_tripdata_2019_01
WHERE
      lpep_pickup_datetime >= '2019-01-15'
  AND lpep_pickup_datetime < '2019-01-16'
  AND lpep_dropoff_datetime >= '2019-01-15'
  AND lpep_dropoff_datetime < '2019-01-16'
;


-- Question 4: Largest trip for each day (Multiple choice)
-- Which was the day with the largest trip distance?
-- *
-- 2019-01-18
-- 2019-01-28
-- 2019-01-15 +
-- 2019-01-10
WITH
    days(date) AS (
    SELECT CAST(date AS DATE) AS date
    FROM
        (
        VALUES
            ('2019-01-28')
          , ('2019-01-15')
          , ('2019-01-18')
          , ('2019-01-10')
        ) AS days(date)
                  )
SELECT
    date
  , MAX(trip_distance) AS max_trip_distance
FROM
    days
    JOIN green_tripdata_2019_01 AS t
         ON t.lpep_pickup_datetime >= days.date
             AND lpep_dropoff_datetime < days.date + 1
GROUP BY
    1
ORDER BY
    2 DESC
LIMIT 1;


-- Question 5: The number of passengers  (Multiple choice)
-- In 2019-01-01 how many trips had 2 and 3 passengers?
-- *
-- 2: 1282 ; 3: 266
-- 2: 1532 ; 3: 126
-- 2: 1282 ; 3: 254 +
-- 2: 1282 ; 3: 274
SELECT
    passenger_count
  , COUNT(*) AS cnt
FROM
    green_tripdata_2019_01
WHERE
      lpep_pickup_datetime >= '2019-01-01'
  AND lpep_pickup_datetime < '2019-01-02'
GROUP BY
    passenger_count
HAVING
    passenger_count IN (2, 3);


-- Question 6: Largest tip (Multiple choice)
-- For the passengers picked up in the Astoria Zone which was the drop up zone that had the largest tip?
-- *
-- Central Park
-- Jamaica

-- South Ozone Park
-- Long Island City/Queens Plaza +
SELECT
    do_z."Zone"
  , MAX(tip_amount) AS largest_tip
FROM
    green_tripdata_2019_01 AS g
    JOIN taxi_zone_lookup  AS pu_z
         ON g."PULocationID" = pu_z."LocationID"
    JOIN taxi_zone_lookup  AS do_z
         ON g."DOLocationID" = do_z."LocationID"
WHERE
    pu_z."Zone" = 'Astoria'
GROUP BY
    1
ORDER BY
    largest_tip DESC
LIMIT 1;
