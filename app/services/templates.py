# ---------------------------------------------------------------------------- #

import logging

# ---------------------------------------------------------------------------- #

from fastapi.templating import Jinja2Templates
from functools import lru_cache
from app.services import get_configuration

# ---------------------------------------------------------------------------- #

logger = logging.getLogger("app.services")

# ---------------------------------------------------------------------------- #


@lru_cache
def get_templates() -> Jinja2Templates:
    """
    Returns a Jinja2Templates instance configured with the templates directory.
    """
    config = get_configuration()

    return Jinja2Templates(directory=config.templates.directory)

# ---------------------------------------------------------------------------- #
