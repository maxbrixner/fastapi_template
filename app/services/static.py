# ---------------------------------------------------------------------------- #

import logging

# ---------------------------------------------------------------------------- #

from typing import Any, Dict
from fastapi import Response
from fastapi.staticfiles import StaticFiles
from starlette.types import Scope
from app.services.config import get_configuration

# ---------------------------------------------------------------------------- #

logger = logging.getLogger("app.core")

# ---------------------------------------------------------------------------- #


class StaticFilesWithHeaders(StaticFiles):
    """
    Custom StaticFiles class to add headers to static file responses.
    """
    _custom_headers: Dict[str, str]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        config = get_configuration()

        self._custom_headers = config.static_files.headers

        logger.info("Static file serving initialized.")

    async def get_response(self, path: str, scope: Scope) -> Response:
        """
        Override the get_response method to add custom headers.
        """
        response = await super().get_response(path, scope)

        if response.status_code == 200:
            for header, value in self._custom_headers.items():
                response.headers[header] = value

        return response

# ---------------------------------------------------------------------------- #
