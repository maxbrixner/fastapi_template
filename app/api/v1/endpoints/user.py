# ---------------------------------------------------------------------------- #

import fastapi
from typing import Dict

# ---------------------------------------------------------------------------- #

from app.database import DatabaseDependency
from app.schemas.user import *
from app.crud.user import *

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(prefix="/user", tags=["user"])

# ---------------------------------------------------------------------------- #


@router.post("/login")
async def user_login() -> None:
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
