from pydantic import BaseModel, Field


class AIToolCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5, max_length=500)
    required_plans: list[str] = []


class AIToolUpdate(BaseModel):
    description: str | None = Field(
        default=None,
        min_length=5,
        max_length=500
    )
    required_plans: list[str] | None = None
    status: str | None = None