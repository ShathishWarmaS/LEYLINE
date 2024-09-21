import os
from datetime import datetime

def get_version_info(api_version: str):
    is_kubernetes = os.getenv("KUBERNETES_SERVICE_HOST") is not None
    current_date = int(datetime.now().timestamp())
    
    return {
        "version": api_version,
        "date": current_date,
        "kubernetes": is_kubernetes
    }

async def shutdown_event():
    from app.database import database
    await database.disconnect()
