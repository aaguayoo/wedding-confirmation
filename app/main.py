"""Wedding Confirmation - API main app."""

from fastapi import FastAPI  # type: ignore

from app.api.v1.routers import wedding-confirmation as v1_wedding-confirmation
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Registrar routers para cada versión
app.include_router(
    v1_wedding-confirmation.router, 
    prefix="/v1/wedding-confirmation", 
    tags=["Wedding Confirmation v1"],
)


@app.get("/")
def read_root() -> dict:
    """Read root."""
    return {"message": "API with versioning is running"}
