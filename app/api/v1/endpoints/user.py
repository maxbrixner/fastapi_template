# ---------------------------------------------------------------------------- #

import fastapi
from typing import Dict

# ---------------------------------------------------------------------------- #

import app.schemas as schemas
import app.crud as crud
from app.database import DatabaseDependency

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
    user: schemas.user.UserCreateSchema,
    session: DatabaseDependency
) -> Dict:
    """
    Create a new user.
    """
    crud.user.create_user(session=session, user=user)
    return {"message": f"User '{user.username}' created successfully."}

# ---------------------------------------------------------------------------- #
