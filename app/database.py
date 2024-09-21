import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, TIMESTAMP, func, text
from sqlalchemy.exc import ProgrammingError
from databases import Database
import logging
from app.models import DomainQuery 

logging.basicConfig(level=logging.INFO)

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a Database instance
database = Database(DATABASE_URL)

# Create SQLAlchemy metadata instance
metadata = MetaData()

# Define your table structure
lookup_logs = Table(
    "lookup_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("domain", String),
    Column("ipv4_addresses", String),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
    Column("client_ip", String, nullable=True)
)

# Create an engine
engine = create_engine(DATABASE_URL)

# Connection functions
async def connect():
    await database.connect()

async def disconnect():
    await database.disconnect()

# Function to ensure the client_ip column exists
def ensure_client_ip_column_exists():
    with engine.connect() as connection:
        try:
            connection.execute(text("""
                DO $$ 
                BEGIN 
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM information_schema.columns 
                        WHERE table_name='lookup_logs' 
                        AND column_name='client_ip'
                    ) THEN
                        ALTER TABLE lookup_logs ADD COLUMN client_ip VARCHAR;
                    END IF;
                END $$;
            """))
        except ProgrammingError as e:
            print(f"An error occurred: {e}")

# Ensure the client_ip column exists
ensure_client_ip_column_exists()

# Function to save a query in the database
async def save_query(domain: str, ipv4_addresses: list[str], client_ip: str):
    query = lookup_logs.insert().values(
        domain=domain,
        ipv4_addresses=",".join(ipv4_addresses),
        client_ip=client_ip
    )
    await database.execute(query)

# Function to get query history from the database
async def get_query_history(limit: int = 20):
    try:
        query = lookup_logs.select().order_by(lookup_logs.c.timestamp.desc()).limit(limit)
        result = await database.fetch_all(query)
        print("Query history fetched successfully.")
        # Transforming the result into DomainQuery format
        return [
            DomainQuery(
                addresses=[{"ip": ip, "queryID": record["id"]} for ip in record["ipv4_addresses"].split(",")],
                created_time=int(record["timestamp"].timestamp()),  # Assuming timestamp is a datetime object
                queryID=record["id"],
                client_ip=record["client_ip"],
                domain=record["domain"]
            ) for record in result
        ]
    except Exception as e:
        print(f"Error fetching query history: {e}")
        raise
