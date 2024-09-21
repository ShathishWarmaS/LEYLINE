from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, TIMESTAMP, func
from databases import Database
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/domain_lookup")

database = Database(DATABASE_URL)
metadata = MetaData()

lookup_logs = Table(
    "lookup_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("domain", String),
    Column("ipv4_addresses", String),
    Column("timestamp", TIMESTAMP, server_default=func.now())
)

async def save_query(domain: str, ipv4_addresses: list[str]):
    query = lookup_logs.insert().values(domain=domain, ipv4_addresses=",".join(ipv4_addresses))
    await database.execute(query)

async def get_query_history(limit: int = 20):
    query = lookup_logs.select().order_by(lookup_logs.c.timestamp.desc()).limit(limit)
    return await database.fetch_all(query)
