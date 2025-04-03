# ---------------------------------------------------------------------------- #

import fastapi
import sqlmodel
from typing import Annotated

# ---------------------------------------------------------------------------- #

from .database import database

# ---------------------------------------------------------------------------- #


DatabaseDependency = Annotated[
    sqlmodel.Session, fastapi.Depends(database.get_session)
]

# ---------------------------------------------------------------------------- #
