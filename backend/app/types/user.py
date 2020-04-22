from typing import Optional

from pydantic.main import BaseModel


class UserAuthForm(BaseModel):
    username: str
    password: str


class EditUserForm(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]


class UserType(BaseModel):
    id: int
    username: str
    password: str
    email: Optional[str]


class RefreshTokenData(BaseModel):
    token: str
