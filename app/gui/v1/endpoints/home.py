# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

import app.schemas as schemas
import app.services as services

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(prefix="/home", tags=[schemas.Tags.gui])

# ---------------------------------------------------------------------------- #


@router.get("", summary="Home Gui Page")
async def home_gui_page(
    request: fastapi.Request,
    templates: services.TemplatesDependency,
) -> fastapi.responses.HTMLResponse:
    """
    Displays a home GUI page.
    """
    return templates.TemplateResponse(
        "home.html",
        context={
            "request": request
        }
    )

# ---------------------------------------------------------------------------- #
