from pydantic import BaseModel, Field


class PlanCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    monthly_price: float = Field(..., ge=0)
    daily_request_limit: int | None = Field(
        default=None,
        ge=0
    )
    available_ai_models: list[str] = []
    file_upload_limit: int = Field(
        default=0,
        ge=0
    )
    features: list[str] = []


class PlanUpdate(BaseModel):
    monthly_price: float | None = Field(
        default=None,
        ge=0
    )
    daily_request_limit: int | None = Field(
        default=None,
        ge=0
    )
    available_ai_models: list[str] | None = None
    file_upload_limit: int | None = Field(
        default=None,
        ge=0
    )
    features: list[str] | None = None
    status: str | None = None