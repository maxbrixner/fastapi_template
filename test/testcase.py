# ---------------------------------------------------------------------------- #

import unittest
import sqlmodel
import sqlmodel.pool
import sqlalchemy
import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

# ---------------------------------------------------------------------------- #

from app import create_app
from app.database import database

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
    api_version: str

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the test case by creating a FastAPI test client and initializing
        an in-memory SQLite database for testing. This runs once before all
        tests.
        """
        os.environ["CONFIG"] = "config.test.json"
        os.environ["LOGGING"] = "logging.test.json"

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

        def get_session_override() -> sqlmodel.Session:
            return self.session

        self.app.dependency_overrides[
            database.get_session
        ] = get_session_override

    def tearDown(self) -> None:
        """
        Clean up the test case by closing the session and removing the
        dependency override after each test.
        """
        self.session.close()
        self.app.dependency_overrides.pop(database.get_session, None)

# ---------------------------------------------------------------------------- #
