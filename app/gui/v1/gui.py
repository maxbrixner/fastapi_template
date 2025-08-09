# ---------------------------------------------------------------------------- #

import fastapi

# ---------------------------------------------------------------------------- #

import app.schemas as schemas
from app.gui.v1.endpoints import home_router

# ---------------------------------------------------------------------------- #


router = fastapi.APIRouter(
    prefix="/gui/v1",
    tags=[schemas.Tags.gui, schemas.Tags.v1]
)

router.include_router(home_router)


# ---------------------------------------------------------------------------- #
