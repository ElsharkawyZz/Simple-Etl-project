import os
import subprocess
from time import time
import pandas as pd
from sqlalchemy import create_engine
import argparse

def extract_data(url):
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    os.system(f"curl -L {url} -o ./{csv_name}")

    df_iter = pd.read_csv(csv_name,iterator=True,chunksize=500000)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    return df

def ingest_data(params,df):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name

    postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    
    engine = create_engine(postgres_url)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')
    



def main_flow(table_name :str):
   
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')
    args = parser.parse_args()
    raw_data = extract_data(args.url)
    ingest_data(args,raw_data)


if __name__ == '__main__':
    main_flow(table_name ="yellow_taxi_trips")





