from pydantic import BaseModel


class APIKeyResponse(BaseModel):
    message: str
    api_key: str


class APIKeyUsageResponse(BaseModel):
    api_key: str
    status: str
    usage_count: int
    created_at: object
    last_used_at: object | None