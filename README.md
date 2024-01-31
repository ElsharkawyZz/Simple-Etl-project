# Simple Etl Project by `Docker` and `Postgres` and `Python`

## brief description of  project

### Table of Contents
* Introduction
* Prerequisites
* Installation
* Usage



## *Introduction*
Built a robust data pipeline using Docker containers, with PostgreSQL as the database engine and Python for ETL (Extract, Transform, Load) processes. This project is designed to efficiently extract data from web sources and load it into a Dockerized PostgreSQL database using a Python script.

## *Prerequisites*
`Python and Docker,Postgres`

## *Installation*


the first step clone the repo to download it
```bash
Copy code
# Clone the repository
git clone https://github.com/ElsharkawyZz/Simple-Etl-project.git
```
Then change the terminal to the repo dir

```bash
# Change directory
cd /path/to/Simple-Etl-project
 
```
## *Usage*

if you need to add the data to loacal database you can
run this commend
``` bash
URL= 'Data you will need to download and upload'

python ingest_data.py \
  --user=postgres \
  --password='your password' \
  --host=localhost \
  --port=5432 \
  --db=postgres \
  --table_name= 'Table name that you need to create' \
  --url=${URL}
``` 
`The Result`
```
$ psql -U postgres
Password for user postgres:
psql (16.0)
WARNING: Console code page (850) differs from Windows code page (1252)
         8-bit characters might not work correctly. See psql reference
         page "Notes for Windows users" for details.
Type "help" for help.

postgres=# \dt
               List of relations
 Schema |       Name        | Type  |  Owner
--------+-------------------+-------+----------
 public | yellow_taxi_trips | table | postgres
(1 row)


postgres=# Select count(*) from yellow_taxi_trips
postgres-# ;
 count
--------
 500000
(1 row)

```


You can make extranl database by docker and postgres 
``` bash
#run this commend to create the database
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v 'the dir that will be the volume of postgres'
  -p 5432:5432 \
  postgres:13

# run this code to create docker compose
services:
  pgdatabase:
    image: postgres:13
    environment:
    - POSTGRES_USER=root(any user)
    - POSTGRES_PASSWORD=root(any password)
    - POSTGRES_DB=ny_taxi 
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"  
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"   
  
# run this code to add the data to database
URL= 'Data you will need to download and upload'

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name= 'Table name that you need to create' \
  --url=${URL}  

```
`The Ruselt`

```
ny_taxi=# \dt
               List of relations
 Schema |       Name        | Type  |  Owner
--------+-------------------+-------+----------
 public | yellow_taxi_trips | table | ny_taxi
(1 row)


ny_taxi=# Select count(*) from yellow_taxi_trips;
 count
--------
 500000
(1 row)

```



