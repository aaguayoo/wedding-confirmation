"""{{cookiecutter.project_name.title()}} - API main app."""

from fastapi import FastAPI  # type: ignore

from app.api.v1.routers import {{cookiecutter.project_slug}} as v1_{{cookiecutter.project_slug}}
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Registrar routers para cada versión
app.include_router(
    v1_{{cookiecutter.project_slug}}.router, 
    prefix="/v1/{{cookiecutter.project_slug}}", 
    tags=["{{cookiecutter.project_name.title()}} v1"],
)


@app.get("/")
def read_root() -> dict:
    """Read root."""
    return {"message": "API with versioning is running"}
