# ---------------------------------------------------------------------------- #

import fastapi
from typing import Annotated

# ---------------------------------------------------------------------------- #

from ..services import get_configuration, ConfigSchema

# ---------------------------------------------------------------------------- #


ConfigDependency = Annotated[
    ConfigSchema, fastapi.Depends(get_configuration)
]

# ---------------------------------------------------------------------------- #
