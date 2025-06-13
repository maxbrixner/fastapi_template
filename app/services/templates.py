# ---------------------------------------------------------------------------- #

import logging

# ---------------------------------------------------------------------------- #

from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from functools import lru_cache
from app.services import get_configuration
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Awaitable, Callable, Dict

# ---------------------------------------------------------------------------- #

logger = logging.getLogger("app.services")

# ---------------------------------------------------------------------------- #


@lru_cache
def get_templates() -> Jinja2Templates:
    """
    Returns a Jinja2Templates instance configured with the templates directory.
    """
    config = get_configuration()

    return Jinja2Templates(directory=config.templates.directory)

# ---------------------------------------------------------------------------- #


class TemplateHeaderMiddleware(BaseHTTPMiddleware):

    _custom_headers: Dict[str, str]
    _swagger_path: str | None

    def __init__(
        self,
        app: ASGIApp,
        dispatch: Callable[[Request, Callable[[
            Request], Awaitable[Response]]], Awaitable[Response]] | None = None
    ) -> None:
        super().__init__(app, dispatch)

        config = get_configuration()

        self._custom_headers = config.templates.headers
        self._swagger_path = config.project.swagger_path

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)

        if "text/html" in response.headers.get("content-type", "") \
                and request.scope["path"] != self._swagger_path:
            for header, value in self._custom_headers.items():
                response.headers[header] = value

        return response

# ---------------------------------------------------------------------------- #
