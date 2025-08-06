# ---------------------------------------------------------------------------- #

import fastapi
from fastapi.templating import Jinja2Templates
from typing import Annotated

# ---------------------------------------------------------------------------- #

import app.schemas as schemas
from .templates import get_templates
from .config import get_configuration
from .worker import get_worker_pool, WorkerPool

# ---------------------------------------------------------------------------- #


ConfigDependency = Annotated[
    schemas.ConfigSchema, fastapi.Depends(get_configuration)
]

TemplatesDependency = Annotated[
    Jinja2Templates, fastapi.Depends(get_templates)
]

WorkerPoolDependency = Annotated[
    WorkerPool, fastapi.Depends(get_worker_pool)
]

# ---------------------------------------------------------------------------- #
