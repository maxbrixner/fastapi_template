# ---------------------------------------------------------------------------- #

import pydantic

# ---------------------------------------------------------------------------- #


class UserCreateSchema(pydantic.BaseModel):
    """
    Schema for creating a new user.
    """
    username: str
    email: str
    password: str

# ---------------------------------------------------------------------------- #
