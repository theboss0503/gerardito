import os
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: str | None = Header(None, description="API key de autenticacion")):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key invalida o ausente.")
