from datetime import datetime, timezone


def create_subscription_document(
    user_id: str,
    plan_id: str,
    plan_name: str
):
    return {
        "user_id": user_id,
        "plan_id": plan_id,
        "plan_name": plan_name,
        "status": "active",
        "started_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }