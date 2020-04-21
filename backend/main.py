import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.main_endpoints import router

app = FastAPI()

origins = [
    os.getenv("FRONTEND_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router)
