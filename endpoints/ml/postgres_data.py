import psycopg2
import pandas as pd
from dotenv import dotenv_values
config = dotenv_values(".env")

##******** LOAD DATABASE ********##

def get_postgres_data(command):
    # Set up a connection to the postgres server.
    conn_string = "host="+ (config["DATABASE_HOST"] or None) +" port="+ "5432" +" dbname="+ (config["DATABASE_NAME"] or None) +" user=" + (config["DATABASE_USER"] or None) \
    +" password="+ (config["DATABASE_PASS"] or None) +" sslmode=require"
    conn=psycopg2.connect(conn_string)

    data = pd.read_sql(command, conn)

    conn.close()

    return data

def create_postgres_data(insert_query, insert_values):
    try:
        # Set up a connection to the postgres server.
        conn_string = "host="+ (config["DATABASE_HOST"] or None) +" port="+ "5432" +" dbname="+ (config["DATABASE_NAME"] or None) +" user=" + (config["DATABASE_USER"] or None) \
    +" password="+ (config["DATABASE_PASS"] or None) +" sslmode=require"
        
        conn=psycopg2.connect(conn_string)

        # Create a cursor object
        cursor = conn.cursor()
    
        postgres_insert_query = insert_query
        record_to_insert = insert_values
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")



