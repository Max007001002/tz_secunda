from fastapi import FastAPI

from app.api import building_router
from app.core.security import APIKeyMiddleware


app = FastAPI()
app.add_middleware(APIKeyMiddleware)
app.include_router(building_router)
