
# ---------------------------------------------------------------------------- #

import pydantic
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------- #


class _DatabaseSchema(pydantic.BaseModel):
    echo: bool = False
    max_overflow: int = 10
    pool_size: int = 5
    url: str

# ---------------------------------------------------------------------------- #


class _ProjectSchema(pydantic.BaseModel):
    author: str
    description: str
    summary: Optional[str] = None
    terms_of_service: Optional[str] = None
    title: str
    swagger_path: Optional[str] = "/docs"


# ---------------------------------------------------------------------------- #


class _BackendSchema(pydantic.BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    root_path: str = ""
    max_workers: int = 4


# ---------------------------------------------------------------------------- #


class _CorsSchema(pydantic.BaseModel):
    allow_credentials: bool = False
    allow_headers: List[str] = []
    allow_methods: List[str] = []
    allow_origins: List[str] = []
    enabled: bool = True
    expose_headers: List[str] = []
    max_age: Optional[int] = 600


# ---------------------------------------------------------------------------- #

class _StaticFilesSchema(pydantic.BaseModel):
    directory: str = "static"
    enabled: bool = False
    headers: Dict[str, str] = {}
    name: str = "static"
    path: str = "/static"

# ---------------------------------------------------------------------------- #


class _TemplatesSchema(pydantic.BaseModel):
    directory: str = "templates"
    enabled: bool = False
    headers: Dict[str, str] = {}

# ---------------------------------------------------------------------------- #


class _GzipSchema(pydantic.BaseModel):
    compression_level: int = 5
    enabled: bool = False
    minimum_size: int = 1000


# ---------------------------------------------------------------------------- #

class ConfigSchema(pydantic.BaseModel):
    backend: _BackendSchema = _BackendSchema()
    cors: _CorsSchema = _CorsSchema()
    database: _DatabaseSchema
    gzip: _GzipSchema = _GzipSchema()
    project: _ProjectSchema
    static_files: _StaticFilesSchema = _StaticFilesSchema()
    templates: _TemplatesSchema = _TemplatesSchema()

# ---------------------------------------------------------------------------- #
