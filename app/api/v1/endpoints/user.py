# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

from app.database import DatabaseDependency
from app.core import ConfigDependency
from app.schemas.user import *
from app.crud.user import *

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(prefix="/user", tags=["user"])

# ---------------------------------------------------------------------------- #


@router.get("/login")
async def user_login():
    """
    Login a user.
    """
    raise NotImplementedError("Login not implemented yet.")

# ---------------------------------------------------------------------------- #


@router.post("/create")
async def user_create(
    user: UserCreateSchema,
    session: DatabaseDependency,
    config: ConfigDependency
):
    """
    Create a new user.
    """
    create_user(session=session, user=user)
    return {"message": f"User '{user.username}' created successfully."}

# ---------------------------------------------------------------------------- #
