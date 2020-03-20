from fastapi import FastAPI

from app.endpoints.main_endpoints import router

app = FastAPI()

app.include_router(router)
