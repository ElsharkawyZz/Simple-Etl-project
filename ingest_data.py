import os
import subprocess
from time import time
import pandas as pd
from sqlalchemy import create_engine


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

def ingest_data(user,password,host,port,db,table_name,df):
    postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    
    engine = create_engine(postgres_url)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')
    



def main_flow(table_name :str):
    user = "root"
    password = "root"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"
    csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    raw_data = extract_data(csv_url)
    ingest_data(user, password, host, port, db, table_name,raw_data)


if __name__ == '__main__':
    main_flow(table_name ="yellow_taxi_trips")





