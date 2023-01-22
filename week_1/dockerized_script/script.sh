docker build -t taxi_ingest:v001 .

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"

docker run -it \
    --network=2_docker_sql_default \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=2_docker_sql-pgdatabase-1 \
        --port=5432 \
        --db=ny_taxi \
        --table_name=green_taxi_trips \
        --url=${URL}