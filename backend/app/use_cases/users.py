import json
from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext

import settings
from app.exceptions import CredentialsException, UserExistsException
from app.storage.db.database_storage import DatabaseStorage
from app.storage.models import User, Identity
from app.types import UserAuthForm, EditUserForm, UserType
from app.types.identity import LinkedinData
from app.utils.linkedin_validator import validate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


class UserUseCases:
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.storage = DatabaseStorage(User)
        self.secret_key = settings.SECRET_KEY

    def create_new_user(self, form_data: UserAuthForm):
        user = self.storage.get(username=form_data.username)
        if user:
            raise UserExistsException

        new_user = User(
            username=form_data.username,
            password=self._get_password_hash(form_data.password)
        )
        self.storage.create(new_user)

        return self._login_user(form_data.username, form_data.password)

    def update_user(self, user: UserType, form_data: EditUserForm = Body(...)):
        user.email = form_data.email
        if form_data.password:
            user.password = self._get_password_hash(form_data.password)
        return {"user": self.storage.update(user)}

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        return self._get_user_from_jwt(token)

    def login_user(self, form_data: OAuth2PasswordRequestForm):
        return self._login_user(form_data.username, form_data.password)

    def authenticate_linkedin(self, data: LinkedinData):
        storage = DatabaseStorage(Identity)
        response = validate_token(data.token)
        response_data = json.loads(response.text)
        provider_id = response_data["id"]
        identity = storage.get(provider_id=provider_id)
        if identity:
            user = self.storage.get(id=identity.user_id)
            access_token = self._create_access_token(data={"sub": user.username})
            return {"access_token": access_token, "token_type": "bearer", "user": user}
        if data.email:
            user = self.storage.get(email=data.email)
            if user:
                new_identity = Identity(
                    auth_provider="linkedin",
                    provider_id=provider_id,
                    user_id=user.id
                )
                storage.create(new_identity)
                access_token = self._create_access_token(data={"sub": user.username})
                return {"access_token": access_token, "token_type": "bearer", "user": user}
        new_user = self.storage.create(User(
            username=provider_id,
            password=f"social-login@{provider_id}"
        ))
        new_identity = Identity(
            auth_provider="linkedin",
            provider_id=provider_id,
            user_id=new_user.id
        )
        storage.create(new_identity)
        access_token = self._create_access_token(data={"sub": new_user.username})
        return {"access_token": access_token, "token_type": "bearer", "user": new_user}

    def _get_user_from_jwt(self, token):
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

    def _decode_token(self, token):
        return jwt.decode(token, self.secret_key, algorithms=[settings.JWT_ENCODING_ALGORITHM])

    def _login_user(self, username: str, password: str):
        user = self._authenticate_user(username, password)

        if not user:
            raise CredentialsException

        access_token = self._create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer", "user": user}

    def _create_access_token(self, data: dict, expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
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
