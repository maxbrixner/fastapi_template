import fastapi
import pydantic
import fastapi.security
import jwt
from typing import Annotated

from app.models import User


# todo: create security base class and then offer three implementations:
# OAuth2
# BasicHTTP
# Cookies
# PositConnect


class OAuth2PasswordRequestForm(fastapi.security.OAuth2PasswordRequestForm):
    pass


# todo: get this from config and/or environment variables
oauth2_scheme = fastapi.security.OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.",
            "items": "Read items."},
)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    username: str | None = None
    scopes: list[str] = []


async def get_current_user(
    security_scopes: fastapi.security.SecurityScopes,
    token: Annotated[str, fastapi.Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except:
        raise credentials_exception
    user = User(
        username="test",
        email="test@test.de",
        password="testpassword"  # This should be hashed in a real application
    )
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
