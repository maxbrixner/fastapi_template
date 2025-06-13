# ---------------------------------------------------------------------------- #

import fastapi
from unittest.mock import patch
from contextlib import ExitStack

# ---------------------------------------------------------------------------- #

from app.services import ConfigSchema
from test.testcase import TestCase

# ---------------------------------------------------------------------------- #


class TestBase(TestCase):
    """
    Test cases for base functions like lifespan events or config/logging.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        This runs once before all tests to set up the API version for
        all tests in this class.
        """
        super().setUpClass()
        cls.api_version = "/api/v1"

    def test_lifespan(self) -> None:
        """
        Test if the lifespan connects and disconnects the database.
        """
        with ExitStack() as stack:
            mock_config = stack.enter_context(
                patch('app.database.Database.get_configuration',
                      return_value=ConfigSchema())
            )
            mock_connect = stack.enter_context(
                patch('app.database.Database.connect')
            )
            mock_disconnect = stack.enter_context(
                patch('app.database.Database.disconnect')
            )
            mock_config.return_value = ConfigSchema()

            with self.client:
                response = self.client.get(
                    f"{self.api_version}/test/fake-route")

            assert mock_connect.called
            assert mock_disconnect.called
            assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND

# ---------------------------------------------------------------------------- #
