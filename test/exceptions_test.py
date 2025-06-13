# ---------------------------------------------------------------------------- #

import fastapi
from unittest.mock import patch
from fastapi.exceptions import HTTPException

# ---------------------------------------------------------------------------- #

from app.core.exceptions import exception_handler, http_exception_handler
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
        assert response.status_code == fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR

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
        assert response.status_code == fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_invalid_route(self) -> None:
        """
        Test that an invalid route returns a handled error.
        """
        response = self.client.get(f"{self.api_version}/test/fake-route")
        assert response.status_code == fastapi.status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()

# ---------------------------------------------------------------------------- #
