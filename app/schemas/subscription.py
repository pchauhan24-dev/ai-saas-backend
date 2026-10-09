from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    plan_id: str


class SubscriptionResponse(BaseModel):
    message: str
    subscription: dict