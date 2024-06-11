import psycopg2
from psycopg2 import sql
import pandas as pd

def create_db(dbname):
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Create database using psycopg2.sql to safely construct the SQL statement
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        
        print(f"Database {dbname} created successfully.")

    except Exception as e:
        print(f"Operation failed: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def drop_db(dbname):
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Create database using psycopg2.sql to safely construct the SQL statement
        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(dbname)))
        
        print(f"Database {dbname} dropped successfully.")

    except Exception as e:
        print(f"Operation failed: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def transition(query, params=None, dbname='krannet'):
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
        database=dbname,
        user='postgres',
        password='password',
        host='localhost',
        port= '5432')
        
        cursor = connection.cursor()

        # Transition
        cursor.execute(sql.SQL('BEGIN'))

        if not params:
            cursor.execute(sql.SQL(query))
        else: 
            cursor.execute(sql.SQL(query), params)
        
        # Commit transition
        connection.commit()

        print("Transaction committed successfully.")

    except Exception as e:
        connection.rollback()
        print(f"Transaction failed: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def fetch_table_data(table_name, dbname='krannet'):
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
        database=dbname,
        user='postgres',
        password='password',
        host='localhost',
        port= '5432')
        
        # Fetch data using pandas
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, connection)
        
        return df

    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None

    finally:
        if connection:
            connection.close()