from fastapi import HTTPException
from starlette import status

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password.",
    headers={"WWW-Authenticate": "Bearer"}
)

UserExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Such user already exists."
)
