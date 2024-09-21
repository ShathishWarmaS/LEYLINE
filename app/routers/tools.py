from fastapi import APIRouter, HTTPException, Query
import socket
from app.models import ValidateIPRequest, ValidateIPResponse, Query
from app.database import save_query, get_query_history
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.get("/v1/tools/lookup", response_model=Query)
@limiter.limit("5/minute")
async def lookup_domain(domain: str = Query(..., description="Domain name")):
    try:
        ipv4_addresses = socket.gethostbyname_ex(domain)[2]
        ipv4_only = [ip for ip in ipv4_addresses if '.' in ip]

        await save_query(domain, ipv4_only)
        
        return Query(
            addresses=[{"ip": ip, "queryID": 1} for ip in ipv4_addresses],
            client_ip="127.0.0.1",
            created_time=1663534325,
            domain=domain,
            queryID=1
        )
    except socket.gaierror:
        raise HTTPException(status_code=404, detail="Domain not found")

@router.post("/v1/tools/validate", response_model=ValidateIPResponse)
async def validate_ip(request: ValidateIPRequest):
    try:
        socket.inet_aton(request.ip)
        return {"status": True}
    except socket.error:
        return {"status": False}

@router.get("/v1/history", response_model=Query)
async def get_history():
    history = await get_query_history()
    return {"history": history}
