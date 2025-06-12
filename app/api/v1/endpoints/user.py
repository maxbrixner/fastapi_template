# ---------------------------------------------------------------------------- #

import fastapi
from typing import Annotated, Dict

# ---------------------------------------------------------------------------- #

from app.database import DatabaseDependency
from app.core import ConfigDependency
from app.schemas.user import *
from app.crud.user import *
from app.security import OAuth2PasswordRequestForm, CurrentUser

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(prefix="/user", tags=["user"])

# ---------------------------------------------------------------------------- #


@router.get("/login")
async def user_login(
    credentials: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()]
) -> None:
    """
    Login a user.
    """
    raise NotImplementedError("Login not implemented yet.")

# ---------------------------------------------------------------------------- #


@router.post("/create")
async def user_create(
    user: UserCreateSchema,
    session: DatabaseDependency
) -> Dict:
    """
    Create a new user.
    """
    create_user(session=session, user=user)
    return {"message": f"User '{user.username}' created successfully."}

# ---------------------------------------------------------------------------- #


@router.get("/current")
async def user_current(
    session: DatabaseDependency,
    current_user: CurrentUser
) -> Dict:
    """
    Get the current user.
    """
    print(current_user)

# ---------------------------------------------------------------------------- #
