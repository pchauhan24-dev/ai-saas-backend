from fastapi import APIRouter, Depends

from app.schemas.usage import UsageResponse
from app.utils.dependencies import get_current_user
from app.utils.usage import get_user_usage


router = APIRouter(
    prefix="/usage",
    tags=["Usage Tracking"]
)


@router.get(
    "/",
    response_model=UsageResponse
)
def get_usage(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    return get_user_usage(user_id)