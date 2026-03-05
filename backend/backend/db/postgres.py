import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="investing_db",
        user="postgres",
        password="12345",
        port=5432
    )
