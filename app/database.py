import psycopg2
from app.config import PG_CONN_URL

def get_db_connection():
    conn = psycopg2.connect(PG_CONN_URL)
    return conn
