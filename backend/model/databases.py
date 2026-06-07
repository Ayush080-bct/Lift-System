import os
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from psycopg2 import pool

# Load .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Database configuration from environment
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if not DB_PASS:
    print("DB_PASS not found in environment variables. Check your .env file.")

# ✅ FIXED: Use ThreadedConnectionPool instead of single global connection
# This handles concurrent requests safely
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=20,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

def get_connection():
    """Get a connection from the pool. Caller MUST close it when done."""
    return connection_pool.getconn()

def put_connection(conn):
    """Return a connection to the pool."""
    connection_pool.putconn(conn)

def close_all_connections():
    """Close all pool connections (use on app shutdown)."""
    connection_pool.closeall()