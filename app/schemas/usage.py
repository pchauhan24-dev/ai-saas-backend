from pydantic import BaseModel


class UsageResponse(BaseModel):
    plan: str | None
    daily_usage: int
    daily_limit: int | None
    remaining_requests: int | None
    monthly_usage: int
    daily_tokens_used: int
    monthly_tokens_used: int