# ---------------------------------------------------------------------------- #

import sqlalchemy
import sqlmodel
import logging
import re
import os
from typing import Generator

# ---------------------------------------------------------------------------- #

from app.core.config import config

# ---------------------------------------------------------------------------- #


class Database():
    """
    Simple class for managing database connections using sqlmodel.
    """
    _logger: logging.Logger
    _engine: sqlalchemy.engine.base.Engine | None

    def __init__(self) -> None:
        """
        Initialize the Database class.
        """
        self._logger = logging.getLogger("app.core.database")
        self._engine = None

    def connect(self) -> None:
        """
        Connect to the database. This method creates a new database engine
        and initializes the database schema. The  database URL is obtained
        from the configuration. The URL may contain environment variable
        placeholders in the format {{VAR_NAME}} where VAR_NAME is the name
        of the environment variable to be replaced with its value.
        """
        self._engine = sqlmodel.create_engine(
            url=self._get_database_url(),
            echo=config.database.echo,
            pool_size=config.database.pool_size,
            max_overflow=config.database.max_overflow)
        sqlmodel.SQLModel.metadata.create_all(self._engine)
        self._logger.info("Database connection established.")

    def disconnect(self) -> None:
        """
        Disconnect from the database. This method disposes of the database
        engine and closes all connections.
        """
        if self._engine:
            self._engine.dispose()
        self._engine = None
        self._logger.info("Database connection disposed.")

    def get_session(self) -> Generator[sqlmodel.Session]:
        """
        Get a session from the database engine.
        """
        if self._engine is None:
            raise Exception("Database engine is not initialized.")

        with sqlmodel.Session(self._engine) as session:
            self._logger.debug("Database session created.")
            yield session

        self._logger.debug("Database session closed.")

    def _get_database_url(self) -> str:
        """
        Get the database URL from the configuration. Replace any
        environment variable placeholders in the URL with their values.
        If an environment variable is not set, raise an exception. Placeholders
        are in the format {{VAR_NAME}} where VAR_NAME is the name of the
        environment variable to be replaced.
        """
        url = config.database.url

        def replace_env_var(match: re.Match) -> str:
            """
            Replace environment variable placeholders in the URL.
            """
            name = match.group(1)
            value = os.getenv(name, default=None)
            if value is None:
                raise Exception(f"Environment variable '{name}' not set. "
                                f"The database URL cannot be constructed.")
            return value

        url = re.sub(r"{{(\w+)}}", replace_env_var, url)
        return url

# ---------------------------------------------------------------------------- #


database = Database()

# ---------------------------------------------------------------------------- #
