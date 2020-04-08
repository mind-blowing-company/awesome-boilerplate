from typing import Optional

from pydantic import BaseModel


class IdentityType(BaseModel):
    id: int
    user_id: int
    provider_id: str


class SocialAuthData(BaseModel):
    token: str
    email: Optional[str]
