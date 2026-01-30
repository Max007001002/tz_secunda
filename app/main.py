from fastapi import FastAPI

from app.core.security import APIKeyMiddleware


app = FastAPI()
app.add_middleware(APIKeyMiddleware)
