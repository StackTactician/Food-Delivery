import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Connect to default 'postgres' database
        con = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            host='localhost',
            password='Abuja20092006@',
            port='5432'
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'food_delivery'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute('CREATE DATABASE food_delivery')
            print("Database 'food_delivery' created successfully.")
        else:
            print("Database 'food_delivery' already exists.")
            
        cur.close()
        con.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == '__main__':
    create_database()
