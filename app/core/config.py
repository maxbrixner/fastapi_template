# ---------------------------------------------------------------------------- #

import pydantic
import pathlib
import os
import json
import logging
from typing import Any, List, Self

# ---------------------------------------------------------------------------- #


class _ProjectSchema(pydantic.BaseModel):
    name: str
    description: str
    version: str
    author: str


class _BackendSchema(pydantic.BaseModel):
    host: str
    port: int


class _CorsSchema(pydantic.BaseModel):
    allow_origins: List[str]
    allow_credentials: bool
    allow_methods: List[str]
    allow_headers: List[str]


class _ConfigSchema(pydantic.BaseModel):
    project: _ProjectSchema
    backend: _BackendSchema
    cors: _CorsSchema

# ---------------------------------------------------------------------------- #


class Configuration():
    """
    A simple configuration management class. The _ConfigSchema class
    defines the schema for the configuration file. The Configuration class
    loads the configuration file and provides access to its attributes.
    """
    _logger: logging.Logger
    _config: _ConfigSchema | None

    def __init__(self) -> None:
        """
        Initialize the Configuration class.
        """
        self._logger = logging.getLogger("app.core.config")
        self._config = None

    def load_configuration(self) -> None:
        """
        Load the configuration file from the config directory. The filename
        is specified in the CONFIG environment variable.
        """
        filename = os.getenv("CONFIG")

        if not filename:
            raise Exception("CONFIG environment variable not set.")

        config_file = pathlib.Path(__file__).parent.parent / \
            pathlib.Path("config") / \
            pathlib.Path(filename)

        with config_file.open("r") as file:
            content = json.load(file)
            self._config = _ConfigSchema(**content)

        self._logger.info(f"Application configuration loaded.")

    def setup_logging(self) -> None:
        """
        Set up logging configuration. The filename is specified in the
        LOGGING environment variable.
        """
        filename = os.getenv("LOGGING", None)

        if not filename:
            raise Exception("LOGGING environment variable not set.")

        logging_file = pathlib.Path(__file__).parent.parent / \
            pathlib.Path("config") / \
            pathlib.Path(filename)

        with logging_file.open("r") as file:
            content = json.load(file)
            logging.config.dictConfig(content)

        self._logger.info(f"Logging configuration loaded.")

    def get_config(self) -> Self:
        """
        Retrieve self. This method is used to create the FastAPI dependency.
        """
        return self

    def __getattr__(self, name: str) -> Any:
        """
        Get an attribute of the configuration.
        """
        if name == "_config":
            return self.__dict__["_config"]

        if "_config" not in self.__dict__:
            raise Exception("Configuration not loaded.")

        config = self.__dict__["_config"]

        if config is None:
            raise Exception("Configuration not loaded.")

        if not hasattr(config, name):
            raise AttributeError(f"Configuration has no attribute '{name}'.")

        return getattr(config, name)

# ---------------------------------------------------------------------------- #


config = Configuration()

# ---------------------------------------------------------------------------- #
