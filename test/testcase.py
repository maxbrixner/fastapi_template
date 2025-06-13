# ---------------------------------------------------------------------------- #

import unittest
import sqlmodel
import sqlmodel.pool
import sqlalchemy

from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

from typing import Generator

# ---------------------------------------------------------------------------- #

from app import create_app
from app.database import get_database_session, Database
from app.services import get_configuration, ConfigSchema

# ---------------------------------------------------------------------------- #


class TestCase(unittest.TestCase):
    """
    Base test case class for setting up a FastAPI test client and an
    in-memory SQLite database for testing. This class provides setup and
    teardown methods to ensure a clean state for each test.
    """
    app: FastAPI
    client: TestClient
    engine: sqlalchemy.engine.base.Engine
    session: sqlmodel.Session
    api_version: str

    config_patcher: unittest.mock._patch
    logging_patcher: unittest.mock._patch

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the test case by creating a FastAPI test client and initializing
        an in-memory SQLite database for testing. This runs once before all
        tests.
        """
        cls.config_patcher = patch(
            'app.core.app.get_configuration', return_value=ConfigSchema())
        cls.config_patcher.start()

        cls.logging_patcher = patch(
            'app.core.app.setup_logger')
        cls.logging_patcher.start()

        cls.app = create_app()

        cls.client = TestClient(cls.app)

        cls.engine = sqlmodel.create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=sqlmodel.pool.StaticPool,
        )

        cls.api_version = ""

    def setUp(self) -> None:
        """
        Set up the test case by initializing the SQLite database for testing.
        This runs before each test to ensure a clean state.
        """
        sqlmodel.SQLModel.metadata.drop_all(self.engine)
        sqlmodel.SQLModel.metadata.create_all(self.engine)

        self.session = sqlmodel.Session(self.engine)

        def get_session_override() -> Generator[sqlmodel.Session]:
            yield self.session

        def get_config_override() -> ConfigSchema:
            return ConfigSchema()

        self.app.dependency_overrides[
            get_database_session
        ] = get_session_override

        self.app.dependency_overrides[
            get_configuration
        ] = get_config_override

    def tearDown(self) -> None:
        """
        Clean up the test case by closing the session and removing the
        dependency override after each test.
        """
        self.session.close()
        self.app.dependency_overrides.pop(Database.get_session, None)
        self.app.dependency_overrides.pop(get_configuration, None)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up the test case by closing the session and removing the
        dependency override after each test.
        """
        cls.config_patcher.stop()
        cls.logging_patcher.stop()
        super().tearDownClass()

# ---------------------------------------------------------------------------- #
