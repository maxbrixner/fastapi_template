# ---------------------------------------------------------------------------- #

import sqlalchemy
import sqlmodel
import logging
from typing import Generator

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
        and initializes the database schema.
        """
        self._engine = sqlmodel.create_engine("sqlite:///database.db")
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

# ---------------------------------------------------------------------------- #


database = Database()

# ---------------------------------------------------------------------------- #
