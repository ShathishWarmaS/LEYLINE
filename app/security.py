import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

def setup_security_headers(app: FastAPI, allowed_origin: str):
    # Redirect HTTP to HTTPS
    app.add_middleware(HTTPSRedirectMiddleware)

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[allowed_origin] if allowed_origin != "*" else CORS_ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Secure Headers
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self';"
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response
