from pydantic import BaseModel

class Status(BaseModel):
    date: int
    kubernetes: bool
    version: str

class HealthStatus(BaseModel):
    status: str

class ValidateIPRequest(BaseModel):
    ip: str

class ValidateIPResponse(BaseModel):
    status: bool

class Address(BaseModel):
    ip: str
    queryID: int

class Query(BaseModel):
    addresses: list[Address]
    client_ip: str
    created_time: int
    domain: str
    queryID: int

class HTTPError(BaseModel):
    message: str
