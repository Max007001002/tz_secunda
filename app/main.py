from fastapi import FastAPI

from app.api import activity_router, building_router, organization_router
from app.core.security import APIKeyMiddleware


app = FastAPI()
app.add_middleware(APIKeyMiddleware)
app.include_router(activity_router)
app.include_router(building_router)
app.include_router(organization_router)
