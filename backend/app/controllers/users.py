import json
from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext

import settings
from app.exceptions import CredentialsException, UserExistsException
from app.storage.db.database_storage import DatabaseStorage
from app.storage.models import User, Identity
from app.types import UserAuthForm, EditUserForm, UserType, SocialAuthData
from app.utils.social_token_validator import validate_linkedin, validate_google, validate_facebook

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


class UsersController:
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.users_storage = DatabaseStorage(User)
        self.identities_storage = DatabaseStorage(Identity)

    def create_new_user(self, form_data: UserAuthForm):
        user = self.users_storage.get(username=form_data.username)
        if user:
            raise UserExistsException

        new_user = User(
            username=form_data.username,
            password=self._get_password_hash(form_data.password)
        )
        self.users_storage.create(new_user)

        return self._login_user(form_data.username, form_data.password)

    def update_user(self, user: UserType, form_data: EditUserForm):
        user.username = form_data.username if form_data.username else user.username
        user.email = form_data.email if form_data.email else user.email
        user.password = self._get_password_hash(form_data.password) if form_data.password else user.password

        updated_user = self.users_storage.update(user)
        return self._create_auth_response(token_data={"sub": user.username}, user=updated_user)

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        return self._get_user_from_jwt(token)

    def login_user(self, form_data: OAuth2PasswordRequestForm):
        return self._login_user(form_data.username, form_data.password)

    def authenticate_linkedin(self, data: SocialAuthData):
        response = json.loads(validate_linkedin(data.token).text)
        return self._authenticate_social_account(data, response)

    def authenticate_google(self, data: SocialAuthData):
        response = json.loads(validate_google(data.token).text)
        return self._authenticate_social_account(data, response)

    def authenticate_facebook(self, data: SocialAuthData):
        response = json.loads(validate_facebook(data.token).text)
        return self._authenticate_social_account(data, response)

    def validate_refresh_token(self, token: str = Depends(oauth2_scheme)):
        payload = self._get_payload_from_token(token)
        owner_username = payload.get("owner")

        if owner_username is None:
            raise CredentialsException

        user = self.users_storage.get(username=owner_username)

        if user is None:
            raise CredentialsException

        return self._create_auth_response(token_data={"sub": user.username}, user=user)

    def _authenticate_social_account(self, data: SocialAuthData, response: dict):
        email = data.email if "email" not in response.keys() else response["email"]
        provider_id = response["id"]

        if email:
            user = self.users_storage.get(email=email)
            if user:
                return self._create_auth_response(token_data={"sub": user.username}, user=user)

        identity = self.identities_storage.get(provider_id=provider_id)

        if identity:
            user = self.users_storage.get(id=identity.user_id)
            return self._create_auth_response(token_data={"sub": user.username}, user=user)

        user_to_create = User(username=provider_id, password=self._get_password_hash(provider_id))

        if email:
            user_to_create.email = email

        new_user = self.users_storage.create(user_to_create)
        identity_to_create = Identity(user_id=new_user.id, provider_id=provider_id)
        self.identities_storage.create(identity_to_create)

        return self._create_auth_response(token_data={"sub": new_user.username}, user=new_user)

    def _get_user_from_jwt(self, token):
        payload = self._get_payload_from_token(token)
        username: str = payload.get("sub")

        if username is None:
            raise CredentialsException

        user = self.users_storage.get(username=username)

        if user is None:
            raise CredentialsException

        return user

    def _get_payload_from_token(self, token):
        try:
            payload = self._decode_token(token)
        except PyJWTError as e:
            print(e)
            raise CredentialsException
        return payload

    def _decode_token(self, token):
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ENCODING_ALGORITHM])

    def _login_user(self, username: str, password: str):
        user = self._authenticate_user(username, password)

        if not user:
            raise CredentialsException

        return self._create_auth_response(token_data={"sub": user.username}, user=user)

    def _create_auth_response(self, token_data, user):
        access_token = self._create_jwt(data=token_data)
        refresh_token = self._generate_refresh_token(user)

        return {
            "token_type": "bearer",
            "access_token": access_token,
            "user": user,
            "refresh_token": refresh_token
        }

    def _generate_refresh_token(self, user):
        refresh_token = self._create_jwt(data={"owner": user.username}, expire_minutes=43200)
        return refresh_token

    def _create_jwt(self, data: dict, expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
        data_to_encode = data.copy()
        expiration_time = datetime.utcnow() + timedelta(expire_minutes)
        data_to_encode.update({"exp": expiration_time})
        encoded_jwt = jwt.encode(
            data_to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ENCODING_ALGORITHM
        )

        return encoded_jwt

    def _authenticate_user(self, username: str, password: str) -> User:
        user = self.users_storage.get(username=username)

        if user and self._verify_password(password, user.password):
            return user

    def _verify_password(self, plain_password: str, hashed_password: str):
        return self.password_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str):
        return self.password_context.hash(password)
