# ---------------------------------------------------------------------------- #

import fastapi
import sqlmodel
from typing import Annotated

# ---------------------------------------------------------------------------- #

from .config import config

# ---------------------------------------------------------------------------- #


ConfigDependency = Annotated[
    sqlmodel.Session, fastapi.Depends(config.get_config)
]

# ---------------------------------------------------------------------------- #
