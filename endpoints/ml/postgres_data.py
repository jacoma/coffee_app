import psycopg2
import os
import pandas as pd

##******** LOAD DATABASE ********##

def get_postgres_data(command):
    # Set up a connection to the postgres server.
    conn_string = "host="+ os.getenv("DATABASE_HOST", None) +" port="+ "5432" +" dbname="+ os.getenv("DATABASE_NAME", None) +" user=" + os.getenv("DATABASE_USER", None) \
    +" password="+ os.getenv("DATABASE_PASS", None)+" sslmode=require"
    conn=psycopg2.connect(conn_string)

    # Create a cursor object
    cursor = conn.cursor()

    data = pd.read_sql(command, conn)

    conn.close()

    return data

def create_postgres_data(insert_query, insert_values):
    try:
        # Set up a connection to the postgres server.
        conn_string = "host="+ os.getenv("DATABASE_HOST", None) +" port="+ "5432" +" dbname="+ os.getenv("DATABASE_NAME", None) +" user=" + os.getenv("DATABASE_USER", None) \
        +" password="+ os.getenv("DATABASE_PASS", None)+" sslmode=require"
        
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
        print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")



