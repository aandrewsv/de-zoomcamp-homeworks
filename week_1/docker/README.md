The name of the folder docker_compose/myapp sets the name of the docker network: myapp_default

Inside of docker_compose folder run first:


```bash
docker-compose up -d
```

You have now both containers running with database and pgadmin, we have to populate the db now

Run first to build the image with the current script (ingest_data.py)
```bash
docker build -t taxi_ingest:v001 .
```

Run the following script and remember to double check all the parameters.

If myapp folder name was modified the  name of network and database host will change accordingly.

After running the command check the schema that is printed and if its all good enter "y" to accept it and populate the database table
 
If modifications must be done to those data types, enter "n" or any input. Process will stop anyways unless you enter "y"

Go to ingest_data.py script and modify the schema to your needs updating the pandas dataframe chunk passed to adjustDataTypes function

Remember that if ingest_data was modified you'll have to build the image again with the last command



Define the url from where the data will be downloaded
```bash
URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
```


```bash
docker run -it \
    --network=myapp_default \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=myapp-pgdatabase-1 \
        --port=5432 \
        --db=ny_taxi \
        --table_name=taxi_zone_lookups \
        --url=${URL}
```

[Green taxi trips url here](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz)


