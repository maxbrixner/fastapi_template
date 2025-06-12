# ---------------------------------------------------------------------------- #

import fastapi
import sqlmodel
from typing import Annotated

# ---------------------------------------------------------------------------- #

from app.models import User
from .security import get_current_user

# ---------------------------------------------------------------------------- #

CurrentUser = Annotated[User, fastapi.Depends(get_current_user)]

# ---------------------------------------------------------------------------- #
