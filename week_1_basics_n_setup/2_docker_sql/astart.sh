# run dockered postgres
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

#cga  docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres

# run dockered pgAdmin
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4

#docker build

#
##
python3 ingest_data.py --user root --password root --host localhost --port 5432 \
  --db ny_taxi --table_name test_tbl_1 \
  --url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz


# --user root --password root --host localhost --port 5432 --db ny_taxi --table_name test_tbl_1  --url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz