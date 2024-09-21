import os
from fastapi import FastAPI, HTTPException, Query
from app.models import Status, HealthStatus, ValidateIPRequest, ValidateIPResponse, Query
from app.database import save_query, get_query_history
from app.security import setup_security_headers
from app.logging_config import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import socket
from dotenv import load_dotenv
import os

load_dotenv()  # Take environment variables from .env.

#SERVICE_PORT = int(os.getenv("SERVICE_PORT", 3000))

# Environment Variables
DOMAIN = os.getenv("DOMAIN", "localhost")
API_VERSION = os.getenv("API_VERSION", "0.1.0")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 3000))

# Initialize the FastAPI app
app = FastAPI()

# Setup logging
setup_logging()

# Prometheus instrumentation
Instrumentator().instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")

# Security middleware for headers and host validation
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=[DOMAIN, f"*.{DOMAIN}", "localhost"]
)
setup_security_headers(app, allowed_origin=f"https://{DOMAIN}")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/", response_model=Status, summary="Show current status", tags=["status"])
async def query_status():
    return {
        "date": 1663534325,
        "kubernetes": False,
        "version": API_VERSION
    }

@app.get("/health", response_model=HealthStatus, summary="Show health status", tags=["health"])
async def query_health():
    return {"status": "OK"}

@app.get("/v1/history", response_model=Query, summary="List queries", tags=["history"])
async def queries_history():
    # Example data, replace with actual database logic
    return Query(
        addresses=[{"ip": "127.0.0.1", "queryID": 1}],
        client_ip="127.0.0.1",
        created_time=1663534325,
        domain="example.com",
        queryID=1
    )

@app.get("/v1/tools/lookup", response_model=Query, summary="Lookup domain", tags=["tools"])
@limiter.limit("5/minute")
async def lookup_domain(domain: str = Query(..., description="Domain name")):
    try:
        ipv4_addresses = socket.gethostbyname_ex(domain)[2]
        await save_query(domain, ipv4_addresses)
        return Query(
            addresses=[{"ip": ip, "queryID": 1} for ip in ipv4_addresses],
            client_ip="127.0.0.1",
            created_time=1663534325,
            domain=domain,
            queryID=1
        )
    except socket.gaierror:
        raise HTTPException(status_code=404, detail="Domain not found")

@app.post("/v1/tools/validate", response_model=ValidateIPResponse, summary="Simple IP validation", tags=["tools"])
async def validate_ip(request: ValidateIPRequest):
    try:
        socket.inet_aton(request.ip)
        return {"status": True}
    except socket.error:
        return {"status": False}
