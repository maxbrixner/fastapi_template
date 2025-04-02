# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

from app.core.database import database
from app.schemas.user import *
from app.crud.user import *
from app.schemas.user import *

# ---------------------------------------------------------------------------- #

router = fastapi.APIRouter(prefix="/user", tags=["user"])

# ---------------------------------------------------------------------------- #


@router.get("/login")
async def user_login():
    """
    User login endpoint.
    """
    raise Exception("This is a test exception")
    return {"message": "User login endpoint"}

# ---------------------------------------------------------------------------- #


@router.post("/create")
async def user_create(user: UserCreateSchema):
    """
    Create a new user.
    """
    with database.session() as session:
        create_user(session=session, user=user)
        return {"message": "User created successfully."}

# ---------------------------------------------------------------------------- #
