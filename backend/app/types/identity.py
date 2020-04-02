from typing import Optional

from pydantic import BaseModel


class IdentityType(BaseModel):
    id: int
    user_id: int
    auth_provider: str
    provider_id: str


class LinkedinData(BaseModel):
    token: str
    email: Optional[str]
