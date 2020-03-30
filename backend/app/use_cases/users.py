from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext

import settings
from app.exceptions import CredentialsException, UserExistsException
from app.storage.db.database_storage import DatabaseStorage
from app.storage.models import User
from app.types import UserFormData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


class UserUseCases:
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.storage = DatabaseStorage(User, settings.DATABASE_ENGINE)
        self.secret_key = settings.SECRET_KEY

    def create_new_user(self, form_data: UserFormData):
        user = self.storage.get(username=form_data.username)
        if user:
            raise UserExistsException

        new_user = User(
            username=form_data.username,
            password=self._get_password_hash(form_data.password)
        )
        self.storage.create(new_user)

        return self._login_user(form_data.username, form_data.password)

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = self._decode_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException
        except PyJWTError:
            raise CredentialsException

        user = self.storage.get(username=username)

        if user is None:
            raise CredentialsException

        return user

    def login_user(self, form_data: OAuth2PasswordRequestForm):
        return self._login_user(form_data.username, form_data.password)

    def _decode_token(self, token):
        return jwt.decode(token, self.secret_key, algorithms=[settings.JWT_ENCODING_ALGORITHM])

    def _login_user(self, username: str, password: str):
        user = self._authenticate_user(username, password)

        if not user:
            raise CredentialsException

        access_token = self._create_access_token(
            data={"sub": user.username},
            expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user}

    def _create_access_token(self, data: dict, expire_minutes: int):
        data_to_encode = data.copy()
        expiration_time = datetime.utcnow() + timedelta(expire_minutes)
        data_to_encode.update({"exp": expiration_time})
        encoded_jwt = jwt.encode(
            data_to_encode,
            self.secret_key,
            algorithm=settings.JWT_ENCODING_ALGORITHM
        )

        return encoded_jwt

    def _authenticate_user(self, username: str, password: str):
        user = self.storage.get(username=username)

        if not user:
            return False
        if not self._verify_password(password, user.password):
            return False

        return user

    def _verify_password(self, plain_password: str, hashed_password: str):
        return self.password_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str):
        return self.password_context.hash(password)
