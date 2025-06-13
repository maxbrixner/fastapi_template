# ---------------------------------------------------------------------------- #

import logging
import pydantic
import pathlib
import os
import json
from typing import List, Optional
from functools import lru_cache

# ---------------------------------------------------------------------------- #

logger = logging.getLogger("app.services")

# ---------------------------------------------------------------------------- #


class _DatabaseSchema(pydantic.BaseModel):
    url: str = "sqlite:///./test.db"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class _ProjectSchema(pydantic.BaseModel):
    title: str = "Blank Title"
    description: str = "Blank Description"
    version: str = "0.1.0"
    author: str = "Blank Author"


class _BackendSchema(pydantic.BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    root_path: str = ""


class _CorsSchema(pydantic.BaseModel):
    allow_origins: List[str] = []
    allow_credentials: bool = False
    allow_methods: List[str] = []
    allow_headers: List[str] = []
    expose_headers: List[str] = []
    max_age: Optional[int] = 600


class ConfigSchema(pydantic.BaseModel):
    backend: _BackendSchema = _BackendSchema()
    cors: _CorsSchema = _CorsSchema()
    database: _DatabaseSchema = _DatabaseSchema()
    project: _ProjectSchema = _ProjectSchema()

# ---------------------------------------------------------------------------- #


@lru_cache
def get_configuration() -> ConfigSchema:
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
