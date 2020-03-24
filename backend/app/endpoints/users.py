from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import settings
from app.types import UserFormData, UserType
from app.use_cases.users import login_user, get_current_user, create_new_user

router = APIRouter()


@router.get("/current")
def get_current_user(current_user: UserType = Depends(get_current_user)):
    return current_user


@router.post(settings.TOKEN_URL)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data)


@router.post("/register")
def create_user(form_data: UserFormData):
    return create_new_user(form_data)
