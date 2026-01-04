"""Base models."""

from pydantic import BaseModel


class BaseRequest(BaseModel):
    """Base request."""

    request: str


class BaseResponse(BaseModel):
    """Base response."""

    request: str
    response: str
