## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL

## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

**Runned:**
```bash
docker build --help
```
**In the Output:**

```bash
        --iidfile string          Write the image ID to the file
```

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- **`--iidfile string`(X)**
- `--idimage string`
- `--idfile string`


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

**Runned:**
```bash
sudo docker run -it python:3.9 bash
```

**Then inside container**:
```bash
pip list
```

**Output:**
```bash
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```

- 1
- 6
- **3(X)**
- 7

## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.


**Runned:**
```sql
SELECT COUNT(*) FROM green_taxi_data
 WHERE date(lpep_pickup_datetime) = date '2019-01-15' 
 AND date(lpep_dropoff_datetime) = date '2019-01-15';
```

**Output:**
```bash
+-------+
| count |
|-------|
| 20530 |
+-------+
SELECT 1
Time: 0.065s
```

- 20689
- **20530(X)**
- 17630
- 21090


## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

**Runned:**
```sql
SELECT lpep_pickup_datetime, trip_distance FROM green_taxi_data ORDER BY trip_distance DESC limit 1;
```

**Output:**
```bash
+----------------------+---------------+
| lpep_pickup_datetime | trip_distance |
|----------------------+---------------|
| 2019-01-15 19:27:58  | 117.99        |
+----------------------+---------------+
SELECT 1
Time: 0.093s
```

- 2019-01-18
- 2019-01-28
- **2019-01-15(X)**
- 2019-01-10

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?

**Runned:**
```sql
SELECT COUNT(*) FROM green_taxi_data WHERE date(lpep_pickup_datetime) = date '2019-01-01' AND passenger_count = 2;
```

**Output:**
```bash
+-------+
| count |
|-------|
| 1282  |
+-------+
SELECT 1
Time: 0.062s
```
**Runned:**
```sql
SELECT COUNT(*) FROM green_taxi_data WHERE date(lpep_pickup_datetime) = date '2019-01-01' AND passenger_count = 3;
```

**Output:**
```bash
+-------+
| count |
|-------|
| 254   |
+-------+
SELECT 1
Time: 0.062s
```

- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- **2: 1282 ; 3: 254(X)**
- 2: 1282 ; 3: 274


## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`


**Find LocationID of Astoria Zone**
```sql
SELECT "Zone", "LocationID" FROM taxi_zone_lookup WHERE "Zone" = 'Astoria';
```
**Output:**
```bash
+---------+------------+
| Zone    | LocationID |
|---------+------------|
| Astoria | 7          |
| Astoria | 7          |
| Astoria | 7          |
| Astoria | 7          |
+---------+------------+
SELECT 4
Time: 0.007s
```
**Astoria's LocationID is 7. Now I filter the trips by PULocationID and order them by the biggest tip amount**
```sql
SELECT "PULocationID", "DOLocationID", tip_amount FROM green_taxi_data WHERE "PULocationID" = 7 ORDER BY tip_amount DESC LIMIT 1;
```

**Output:**
```bash
+--------------+--------------+------------+
| PULocationID | DOLocationID | tip_amount |
|--------------+--------------+------------|
| 7            | 146          | 88.0       |
+--------------+--------------+------------+
SELECT 1
Time: 0.061s
```
**Now I have the biggest tip of the pickups in Astoria and its DOLocationID is 146**


**Runned:**
```sql
SELECT "Zone", "LocationID" FROM taxi_zone_lookup WHERE "LocationID" = 146;
```


**Output:**
```bash
+-------------------------------+------------+
| Zone                          | LocationID |
|-------------------------------+------------|
| Long Island City/Queens Plaza | 146        |
| Long Island City/Queens Plaza | 146        |
| Long Island City/Queens Plaza | 146        |
| Long Island City/Queens Plaza | 146        |
+-------------------------------+------------+
SELECT 4
Time: 0.008s
```

- Central Park
- Jamaica
- South Ozone Park
- **Long Island City/Queens Plaza(X)**
