from cProfile import label
import numpy as np
import pandas as pd
from azure.storage.blob import BlockBlobService
from io import StringIO
import re
from pyparsing import LRUMemo
from textblob import TextBlob
from endpoints.ml.postgres_data import get_postgres_data, create_postgres_data
from endpoints.data.functions.clean_data import get_coffee_info, get_clean_varietals, get_cleaned_elevation, get_lemma_tokens
import psycopg2


from dotenv import dotenv_values
config = dotenv_values(".env")

conn_string = "host="+ (config["DATABASE_HOST"] or None) +" port="+ "5432" +" dbname="+ (config["DATABASE_NAME"] or None) +" user=" + (config["DATABASE_USER"] or None) \
+" password="+ (config["DATABASE_PASS"] or None) +" sslmode=require"

new_coffee = pd.read_csv('endpoints\\data\\tmp\\final_coffee.csv', encoding='cp437', header=None)


def upload_new_coffee(row, cursor):

    query = "INSERT INTO coffee_dim_coffee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (int(row[0]), row[1], row[5], row[2], row[6], row[3], row[11], row[9], row[8])

    cursor.execute(query, values)

    conn.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into table")

##***** UPLOAD NEW COFFEE *****##
conn=psycopg2.connect(conn_string)

# Create a cursor object
cursor = conn.cursor()

new_coffee.apply(lambda row: upload_new_coffee(row, cursor), axis=1)

##***** UPLOAD NEW RELATIONSHIP BETWEEN COFFEE AND VARIETALS *****##
db_varietals = get_postgres_data('SELECT * FROM coffee_dim_varietal')
query = "INSERT INTO coffee_dim_coffee_varietals (dim_coffee_id, dim_varietal_id) VALUES (%s, %s)"
conn=psycopg2.connect(conn_string)
cursor = conn.cursor()

def upload_coffee_varietal(row, query=query):

    if type(row[7])==float:
        print('Is nan')
        pass
    else:
        print('split varietals')
        varietals = row[7].split(",")

        for v in varietals:
            print('getting varietal id for: ', v)
            id = db_varietals.loc[db_varietals.varietal == v, 'id'].values[0]
            
            values = (int(row[0]), int(id))

            print('Committing to database')
            cursor.execute(query, values)

            conn.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into table")


new_coffee.iloc[189:,].apply(lambda row: upload_coffee_varietal(row), axis=1)

new_coffee.apply(lambda row: "" if type(row[7])==float else print(row[7]), axis=1)



##***** UPLOAD NEW RELATIONSHIP BETWEEN COFFEE AND NOTES *****##
db_notes = get_postgres_data('SELECT * FROM coffee_dim_notes')
query = "INSERT INTO coffee_dim_coffee_roaster_notes (dim_coffee_id, dim_notes_id) VALUES (%s, %s)"

def upload_coffee_notes(row, query = query):

    if type(row[15])==float:
        print('Is nan')
        pass
    else:
        print('split notes')
        notes = row[15].split(",")

        for note in notes:
            n = note.strip()
            print('getting note id for: ', n)
            id = db_notes.loc[db_notes.flavor_notes == n, 'id'].values[0]

            print('Committing to database')
            values = (int(row[0]), int(id))
            cursor.execute(query, values)

            conn.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into table")

new_coffee = pd.read_csv('endpoints\\data\\tmp\\final_coffee.csv', encoding='cp437', header=None)
conn=psycopg2.connect(conn_string)
cursor = conn.cursor()
new_coffee.iloc[187:,].apply(lambda row: upload_coffee_notes(row), axis=1)

new_coffee.apply(lambda row: print(row[15]), axis = 1)