from pydantic import BaseModel, Field


class AIRequestCreate(BaseModel):
    tool_id: str
    prompt: str = Field(..., min_length=1, max_length=10000)


class AIRequestResponse(BaseModel):
    message: str
    request_id: str
    tool: str
    prompt: str
    response: str
    tokens_used: int


class FavoriteUpdate(BaseModel):
    favorite: bool