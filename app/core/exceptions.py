
# ---------------------------------------------------------------------------- #

import fastapi
import logging

# ---------------------------------------------------------------------------- #

logger = logging.getLogger("app.core")

# ---------------------------------------------------------------------------- #


async def exception_handler(
    request: fastapi.Request,
    exception: Exception
) -> fastapi.responses.JSONResponse:
    """
    Exception handler for all unhandled exceptions.
    """
    logger.warning(
        f"Exception handled: '{exception}' for url '{request.url}'.")
    return fastapi.responses.JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers=None
    )


# ---------------------------------------------------------------------------- #


async def http_exception_handler(
    request: fastapi.Request,
    exception: Exception
) -> fastapi.responses.JSONResponse:
    """
    Exception handler for all unhandled http exceptions.
    """
    logger.warning(
        f"HTTP Exception handled: '{exception}' for url '{request.url}'.")
    return fastapi.responses.JSONResponse(
        status_code=exception.status_code if hasattr(
            exception, 'status_code') else 500,
        content={"detail": str(exception.detail) if hasattr(
            exception, 'detail') else "An error occurred"},
        headers=exception.headers if hasattr(
            exception, 'headers') else None
    )

# ---------------------------------------------------------------------------- #
