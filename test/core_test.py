# ---------------------------------------------------------------------------- #

import fastapi
from fastapi.exceptions import HTTPException
from unittest.mock import patch
from contextlib import ExitStack

# ---------------------------------------------------------------------------- #

from app.core.exceptions import exception_handler, http_exception_handler
from test._testcase import TestCase

# ---------------------------------------------------------------------------- #


class TestLifespan(TestCase):
    """
    Test cases for the lifspan events.
    """

    def test_lifespan(self) -> None:
        """
        Test if the lifespan connects and disconnects the database.
        """
        with ExitStack() as stack:
            mock_connect = stack.enter_context(
                patch('app.database.Database.connect')
            )
            mock_disconnect = stack.enter_context(
                patch('app.database.Database.disconnect')
            )

            with self.client:
                response = self.client.get(
                    f"{self.api_version}/test/fake-route")

            assert mock_connect.called
            assert mock_disconnect.called
            assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND

# ---------------------------------------------------------------------------- #


class TestExceptions(TestCase):
    """
    Test cases for exception handlers in the API.
    """

    async def test_exception_handler(self) -> None:
        """
        Test if the exception handler returns a valid JSON response.
        """
        response = await exception_handler(
            fastapi.Request(
                scope={"type": "http", "path": "/test", "headers": []}),
            Exception("Test exception")
        )

        assert isinstance(response, fastapi.responses.JSONResponse)
        assert response.status_code == fastapi.\
            status.HTTP_500_INTERNAL_SERVER_ERROR

    async def test_http_exception_handler(self) -> None:
        """
        Test if the http exception handler returns a valid JSON response.
        """
        response = await http_exception_handler(
            fastapi.Request(
                scope={"type": "http", "path": "/test", "headers": []}),
            HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="Test HTTP exception"
            )
        )

        assert isinstance(response, fastapi.responses.JSONResponse)
        assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND

        response = await http_exception_handler(
            fastapi.Request(
                scope={"type": "http", "path": "/test", "headers": []}),
            Exception(
                "Test HTTP exception"
            )
        )

        assert isinstance(response, fastapi.responses.JSONResponse)
        assert response.status_code == fastapi.status.\
            HTTP_500_INTERNAL_SERVER_ERROR

    def test_invalid_route(self) -> None:
        """
        Test that an invalid route returns a handled error.
        """
        response = self.client.get(f"/test/fake-route")

        assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()

# ---------------------------------------------------------------------------- #
