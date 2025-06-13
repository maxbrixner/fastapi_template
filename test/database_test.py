# ---------------------------------------------------------------------------- #

import sqlmodel
import sqlalchemy
import os
from unittest.mock import patch
from contextlib import ExitStack
from typing import Generator

# ---------------------------------------------------------------------------- #

from test._testcase import TestCase
from app.database import get_database, Database
from app.services import get_configuration, ConfigSchema

# ---------------------------------------------------------------------------- #


class DatabaseTest(TestCase):
    """
    Test cases for database operations in the API.
    """

    def test_initialize(self) -> None:
        """
        Test case for creating a new user.
        """
        get_database.cache_clear()
        with patch("app.database.Database.get_configuration",
                   return_value=ConfigSchema()):
            database = get_database()

        # at this point, the engine should not be initialized
        assert database._engine is None
        assert isinstance(database, Database)

    def test_get_configuration(self) -> None:
        """
        Test case for getting the database configuration.
        """
        get_database.cache_clear()
        with patch("app.database.database.get_configuration",
                   return_value=ConfigSchema()) as mock_config:
            database = get_database()
            config = database.get_configuration()

        assert isinstance(config, ConfigSchema)

    def test_connect(self) -> None:
        """
        Test case for connecting to the database.
        """
        get_database.cache_clear()
        with ExitStack() as stack:
            mock_config = stack.enter_context(
                patch("app.database.database.get_configuration",
                      return_value=ConfigSchema())
            )
            mock_create_engine = stack.enter_context(
                patch(
                    "app.database.database.sqlmodel.create_engine")
            )
            mock_create_engine.return_value = sqlalchemy.create_engine(
                "sqlite://",
                connect_args={"check_same_thread": False},
                poolclass=sqlmodel.pool.StaticPool,
            )
            database = get_database()
            database.connect()

            assert database._engine is not None
            assert isinstance(database._engine, sqlalchemy.engine.base.Engine)
            mock_create_engine.assert_called_once()

            database.disconnect()

    def test_disconnect(self) -> None:
        """
        Test case for disconnecting from the database.
        """
        get_database.cache_clear()
        with ExitStack() as stack:
            mock_config = stack.enter_context(
                patch("app.database.database.get_configuration",
                      return_value=ConfigSchema())
            )
            mock_create_engine = stack.enter_context(
                patch(
                    "app.database.database.sqlmodel.create_engine")
            )
            mock_create_engine.return_value = sqlalchemy.create_engine(
                "sqlite://",
                connect_args={"check_same_thread": False},
                poolclass=sqlmodel.pool.StaticPool,
            )
            database = get_database()
            database.connect()
            database.disconnect()

        assert database._engine is None

    def test_get_session(self) -> None:
        """
        Test case for getting a database session.
        """
        get_database.cache_clear()
        with ExitStack() as stack:
            mock_config = stack.enter_context(
                patch("app.database.database.get_configuration",
                      return_value=ConfigSchema())
            )
            mock_create_engine = stack.enter_context(
                patch(
                    "app.database.database.sqlmodel.create_engine")
            )
            mock_create_engine.return_value = sqlalchemy.create_engine(
                "sqlite://",
                connect_args={"check_same_thread": False},
                poolclass=sqlmodel.pool.StaticPool,
            )
            database = get_database()
            database.connect()

            session = database.get_session()

            assert isinstance(session, Generator)
            assert isinstance(session.__next__(), sqlmodel.Session)

            database.disconnect()

    def test_get_database_url(self) -> None:
        """
        Test case for getting the database URL.
        """
        get_database.cache_clear()
        with ExitStack() as stack:
            mock_config = stack.enter_context(
                patch("app.database.database.get_configuration",
                      return_value=ConfigSchema())
            )
            mock_env = stack.enter_context(
                patch.dict(os.environ, {"VAR1": "test", "VAR2": "db"})
            )
            database = get_database()

            url = database._resolve_url(url="sqlite:///{{VAR1}}:{{VAR2}}.db")
            assert url == "sqlite:///test:db.db"

            with self.assertRaises(Exception):
                url = database._resolve_url(
                    url="sqlite:///{{VAR1}}:{{VAR3}}.db"
                )

            database.disconnect()


# ---------------------------------------------------------------------------- #
