import os
import sqlite3
import csv
import pandas as pd
from sqlalchemy import create_engine


CWD = os.getcwd()
UPLOAD_FOLDER = os.path.join(CWD, 'uploads')
DATABASE = os.path.join(CWD, 'database.db')
TABLE = 'records'

def get_uploaded_files():
    return [f for f in os.listdir(UPLOAD_FOLDER)]

def get_engine():
    conn = create_engine(f"sqlite:///{DATABASE}")
    return conn

def create_table():
    create_query = f'''create table if not exists {TABLE}(
                id INT,
                first_name VARCHAR,
                last_name VARCHAR,
                street_address VARCHAR,
                state VARCHAR,
                zip INT,
                change_in_purchase_status VARCHAR,
                product_id INT,
                product_name VARCHAR,
                product_purchase_amount INT,
                timestamp DATETIME
            )

            '''
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(create_query)
    engine.dispose()

def read_file(filename):
    columns = ['id', 'first_name', 'last_name', 'street_address', 'state',
               'zip', 'change_in_purchase_status', 'product_id',
               'product_name', 'product_purchase_amount', 'timestamp']

    filename = os.path.join(UPLOAD_FOLDER, filename)
    df = pd.read_csv(filename, sep='\t', names=columns, header=None)
    return df

def upload_file(df, table, connection):
    df.to_sql(table, connection, if_exists='append', index=False)

def read_upload_file(filename, connection):
    df = read_file(filename)
    upload_file(df, TABLE, connection)
    filename = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filename):
        os.remove(filename)
