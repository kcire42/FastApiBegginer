import psycopg2
from psycopg2 import Error
from .config import DBHOST, DBPORT, DBNAME, DBUSER, DBPASSWORD

def create_connection():
    """Create and return a database connection."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DBHOST,
            port=DBPORT,
            database=DBNAME,
            user=DBUSER,
            password=DBPASSWORD
        )
        print("Connection to the database was successful.")
    except Error as e:
        print(f"Error while connecting to the database: {e}")
    return conn