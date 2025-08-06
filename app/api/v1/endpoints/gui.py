# ---------------------------------------------------------------------------- #

import fastapi
from typing import Dict

# ---------------------------------------------------------------------------- #

import app.schemas as schemas
import app.services as services

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(prefix="/gui", tags=[schemas.Tags.gui])

# ---------------------------------------------------------------------------- #


@router.get("/demo", summary="Demo Gui Page")
async def demo_gui_page(
    request: fastapi.Request,
    templates: services.TemplatesDependency,
) -> None:
    """
    Displays a demo GUI page.
    """
    return templates.TemplateResponse(
        "demo.html",
        context={
            "request": request
        }
    )

# ---------------------------------------------------------------------------- #
