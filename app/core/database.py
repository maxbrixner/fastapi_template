# ---------------------------------------------------------------------------- #

import sqlalchemy
import sqlmodel
import logging
import contextlib
from typing import Generator

# ---------------------------------------------------------------------------- #

from app.models import *

# ---------------------------------------------------------------------------- #


class Database():
    """
    Database connection class.
    """
    logger: logging.Logger
    engine: sqlalchemy.engine.base.Engine | None

    def __init__(self):
        self.logger = logging.getLogger("app.core.database")
        self.engine = None

    def connect(self) -> None:
        self.logger.info("Connecting to database...")
        self.engine = sqlmodel.create_engine("sqlite:///database.db")
        sqlmodel.SQLModel.metadata.create_all(self.engine)
        self.logger.info("Database connection established.")

    def disconnect(self) -> None:
        self.logger.info("Disconnecting from database...")
        self.engine = None
        self.logger.info("Database disconnected.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @contextlib.contextmanager
    def session(self) -> Generator[sqlmodel.Session]:
        """
        Get a session from the database engine.
        """
        if self.engine is None:
            raise Exception("Database engine not initialized.")

        with sqlmodel.Session(self.engine) as session:
            yield session

# ---------------------------------------------------------------------------- #


database = Database()

# ---------------------------------------------------------------------------- #
