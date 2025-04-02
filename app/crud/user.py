# ---------------------------------------------------------------------------- #

import sqlmodel

# ---------------------------------------------------------------------------- #

from app.models.user import User
from app.schemas.user import *

# ---------------------------------------------------------------------------- #


def create_user(session: sqlmodel, user: UserCreateSchema) -> User:
    """
    Create a new user in the database.
    """
    user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        disabled=False
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# ---------------------------------------------------------------------------- #
