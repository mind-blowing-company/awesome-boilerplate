from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext

import settings
from app.exceptions import CREDENTIALS_EXCEPTION, USER_EXISTS_EXCEPTION
from app.storage.db.database_storage import DatabaseStorage
from app.storage.models import User
from app.types import UserFormData

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)
user_storage = DatabaseStorage(User, settings.DATABASE_ENGINE)


def create_new_user(form_data: UserFormData):
    user = user_storage.get(username=form_data.username)
    if user:
        raise USER_EXISTS_EXCEPTION
    new_user = User(
        username=form_data.username,
        password=_get_password_hash(form_data.password)
    )
    user_storage.create(new_user)
    return _login_user(form_data.username, form_data.password)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ENCODING_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
    except PyJWTError:
        raise CREDENTIALS_EXCEPTION
    user = user_storage.get(username=username)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user


def login_user(form_data: OAuth2PasswordRequestForm):
    return _login_user(form_data.username, form_data.password)


def _login_user(username: str, password: str):
    user = _authenticate_user(username, password)
    if not user:
        raise CREDENTIALS_EXCEPTION
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = {"access_token": access_token, "token_type": "bearer", "user": user}
    return response


def _create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    data_to_encode = data.copy()
    expiration_time = datetime.utcnow() + expires_delta
    data_to_encode.update({"exp": expiration_time})
    encoded_jwt = jwt.encode(
        data_to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ENCODING_ALGORITHM
    )
    return encoded_jwt


def _verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def _get_password_hash(password: str):
    return password_context.hash(password)


def _authenticate_user(username: str, password: str):
    user = user_storage.get(username=username)
    if not user:
        return False
    if not _verify_password(password, user.password):
        return False
    return user
