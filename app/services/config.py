# ---------------------------------------------------------------------------- #

import logging
import pathlib
import os
import json
from functools import lru_cache

# ---------------------------------------------------------------------------- #

import app.schemas as schemas

# ---------------------------------------------------------------------------- #

logger = logging.getLogger("app.services")

# ---------------------------------------------------------------------------- #


@lru_cache
def get_configuration() -> schemas.ConfigSchema:
    """
    Load the configuration file from the config directory. The filename
    is specified in the CONFIG environment variable. We do not use
    pydantic's BaseSettings here because we want to load the configuration
    from a file rather than environment variables.
    """
    filename = os.getenv("CONFIG")

    if not filename:
        raise Exception("CONFIG environment variable not set.")

    config_file = pathlib.Path(__file__).parent.parent / \
        pathlib.Path("config") / \
        pathlib.Path(filename)

    with config_file.open("r") as file:
        content = json.load(file)
        config = ConfigSchema(**content)

    logger.info(f"Application configuration loaded.")

    return config

# ---------------------------------------------------------------------------- #
