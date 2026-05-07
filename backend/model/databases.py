import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_PASS = os.getenv("DB_PASS")
print(DB_PASS)
conn = psycopg2.connect(
    dbname="lift_system",
    user="ayush",
    password=DB_PASS,
    host="localhost",
    port="5432"
)
