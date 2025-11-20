from fastapi import FastAPI
from app.routes import requests

app = FastAPI(title="Requests Admin Panel")

API_PREFIX = "/api/v1"

app.include_router(
    requests.router, prefix=f"{API_PREFIX}/requests", tags=["Requests"]
)
