"""{{cookiecutter.project_name.title()}} router."""

from fastapi import APIRouter, HTTPException  # type: ignore

from app.api.v1.models.base import BaseRequest, BaseResponse
from {{cookiecutter.project_slug}} import __version__

router = APIRouter()


@router.post("/base_post/", response_model=BaseResponse)
async def get_answer(base_request: BaseRequest) -> BaseResponse:
    """DUMMY DOCSTRING."""
    try:
        return BaseResponse(
            request=base_request.request, 
            response=__version__,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
