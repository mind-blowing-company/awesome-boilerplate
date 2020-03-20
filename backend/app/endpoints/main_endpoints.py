from fastapi import APIRouter
from app.endpoints import users

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
