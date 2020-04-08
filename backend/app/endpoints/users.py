from fastapi import APIRouter, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm

from app.types import UserAuthForm, UserType, EditUserForm
from app.types.identity import SocialAuthData
from app.use_cases.users import UserUseCases

router = APIRouter()
use_cases = UserUseCases()


@router.get("/me")
def get_current_user(current_user: UserType = Depends(use_cases.get_current_user)):
    return {"user": current_user}


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return use_cases.login_user(form_data)


@router.post("/register")
def create_user(data: UserAuthForm):
    return use_cases.create_new_user(data)


@router.put("/update")
def update_user(form_data: EditUserForm = Body(...), user: UserType = Depends(use_cases.get_current_user)):
    return use_cases.update_user(user, form_data)


@router.post("/auth/linkedin")
def authenticate_linkedin(data: SocialAuthData = Body(...)):
    return use_cases.authenticate_linkedin(data)


@router.post("/auth/google")
def authenticate_google(data: SocialAuthData = Body(...)):
    return use_cases.authenticate_google(data)


@router.post("/auth/facebook")
def authenticate_facebook(data: SocialAuthData = Body(...)):
    return use_cases.authenticate_facebook(data)
