from datetime import datetime, timezone


def create_plan_document(
    name: str,
    monthly_price: float,
    daily_request_limit: int | None,
    available_ai_models: list[str],
    file_upload_limit: int,
    features: list[str]
):
    return {
        "name": name,
        "monthly_price": monthly_price,
        "daily_request_limit": daily_request_limit,
        "available_ai_models": available_ai_models,
        "file_upload_limit": file_upload_limit,
        "features": features,
        "status": "active",
        "created_at": datetime.now(timezone.utc)
    }