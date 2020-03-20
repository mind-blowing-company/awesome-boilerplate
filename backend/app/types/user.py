from pydantic.main import BaseModel


# Form data type for user registration.
class UserFormData(BaseModel):
    username: str
    password: str


class UserType(BaseModel):
    username: str
    hashed_password: str
