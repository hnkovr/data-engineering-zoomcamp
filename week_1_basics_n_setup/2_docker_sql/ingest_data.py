#!/usr/bin/env python
# coding: utf-8
# needed args set:
# --user USER --password PASSWORD --host HOST --port PORT --db DB --table_name TABLE_NAME --url URL

import argparse
from time import time

import pandas as pd
import sqlalchemy

from utily import *


def main(params, *,
         url='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz',
         skip_errors=False):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url or url

    csv_name = url.split('/')[-1]

    logi(f"""{params=}
            {user =} 
            {password =}
            {host =} 
            {port =} 
            {db =}
            {table_name =}
            {url = }
    """)

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file

    # ~ log.info(f"{(csv_name := 'output.csv.gz' if url.endswith('.csv.gz') else 'output.csv')=}")

    {
        os.system(f"wget {url} -O {csv_name}"),
        print(f"Loading csv-file <{csv_name}> from <{url}>:..")
    } if not check_file_size(csv_name) \
        else print(f"File <{url}> already exists – skip loading.")
    assert check_file_size(csv_name), (check_file_size, csv_name)
    print(bash(f"ls -lsu {csv_name}"))

    engine = sqlalchemy.create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print(f"Loading <{csv_name}> to pandas-df:..")
    df_iter = None
    try:
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    except:
        fprint(csv_name)
        handle_exc(skip_errors=skip_errors)

    df = next(df_iter)

    if 'lpep_pickup_datetime' in df.columns:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    print(f"Loading pandas-df <\n{str(df)[:222]}...\n> to db-table <{table_name}>:..")
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:

        try:
            t_start = time()

            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            print(
                df.to_sql(name=table_name, con=engine, if_exists='append')
                , end=' ')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file or local file local path')

    args = parser.parse_args()

    main(args)
