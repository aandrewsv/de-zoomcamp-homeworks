#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine, inspect
import requests
import tempfile
import shutil


def main(params):
    """
    Ingest csv or .csv.gz data from url then ingest data to postgres database table.

    This script is called from the command line interface passing the listed parameters and
    inserts all the records in a csv file into a table of a postgres database, please check
    the parameters and examples to learn how to use it. Also you can add content to the 
    adjustDataTypes function to adjust the table schema to your needs.

    Parameters
    ----------
    user : string
        User name for postgres.
    password : string
        Password for postgres.
    host : string
        Host for postgres.
    port : string
        Port for postgres.
    db : string
        Database name for postgres.
    name : string
        Name of the table where we will write the results to.
    url : string
        Url of the csv file.

    Examples
    --------
    $ URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
    $ python ingest_data.py \
          --user=root \
          --password=root \
          --host=localhost \
          --port=5432 \
          --db=ny_taxi \
          --table_name=green_taxi_trips \
          --url=${URL}
    """
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    print('Downloading the file...')
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        if not r.ok:
            raise Exception("Failed to download file")
    except Exception as e:
        print(f"Error occured while downloading the file: {e}")
        return

    # Creating temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            shutil.copyfileobj(r.raw, temp)
            temp.flush()
            temp_file_name = temp.name
    except Exception as e:
        print(f"Error occured while creating the temp file: {e}")
        return

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    inspector = inspect(engine)

    # Checking if table already exists
    if table_name in inspector.get_table_names():
        print(f"Table {table_name} already exists in the database {db}")
        return

    # Checking if its a valid csv or gzip compressed csv file
    if os.path.splitext(url)[-1] == ".gz" and os.path.splitext(os.path.splitext(url)[0])[-1] == ".csv":
        compression = 'gzip'
    elif os.path.splitext(url)[-1] == ".csv":
        compression = None
    else:
        raise ValueError("Invalid file extension, please use .csv or .csv.gz")

    df = pd.read_csv(temp_file_name, chunksize=100000, compression=compression, low_memory=False)

    # Validates the schema
    def validateSchema (df_first_chunk):
        print('Schema of the db table: \n' + pd.io.sql.get_schema(df_first_chunk, name=table_name, con=engine))
        response = input("Do you want to proceed with the schema? (y/n) ")

        if response.lower() == "y":
            print("Proceeding...")

        elif response.lower() == "n":
            print("Exiting...")
            exit()
        else:
            print("Invalid response. Exiting...")
            exit()
    
    # Adjust data types
    def adjustDataTypes (df_chunk):
        # Here adjust the data types of the table to your needs, otherwise ignore and
        # just leave the pass in the function
        
        # df_chunk.lpep_pickup_datetime = pd.to_datetime(df_chunk.lpep_pickup_datetime)
        # df_chunk.lpep_dropoff_datetime = pd.to_datetime(df_chunk.lpep_dropoff_datetime)
        pass
    
    
    print(f'Inserting csv file data to {db} table: {table_name}')
    for i, chunk in enumerate(df):
        t_start = time()
        adjustDataTypes(chunk)
        if i == 0:
            validateSchema(chunk)
            t_start = time()
        chunk.to_sql(con=engine, name=table_name, if_exists='append')
        t_end = time()
        print('Chunk inserted... took %.3f second' % (t_end - t_start))
    print("Data Loaded Successfully")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
