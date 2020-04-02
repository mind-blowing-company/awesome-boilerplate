from typing import Optional

from pydantic.main import BaseModel


class UserAuthForm(BaseModel):
    username: str
    password: str


class EditUserForm(BaseModel):
    email: str
    password: Optional[str]


class UserType(BaseModel):
    id: int
    username: str
    password: str
    email: Optional[str]
