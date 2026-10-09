from datetime import datetime, timezone

from app.database import (
    ai_requests_collection,
    subscriptions_collection,
    plans_collection
)

from bson import ObjectId


def get_today_start():
    now = datetime.now(timezone.utc)

    return datetime(
        now.year,
        now.month,
        now.day,
        tzinfo=timezone.utc
    )


def get_month_start():
    now = datetime.now(timezone.utc)

    return datetime(
        now.year,
        now.month,
        1,
        tzinfo=timezone.utc
    )


def estimate_tokens(text: str) -> int:
    words = len(text.split())

    return max(1, words * 2)


def get_user_usage(user_id: str):

    today_start = get_today_start()
    month_start = get_month_start()

    daily_count = ai_requests_collection.count_documents({
        "user_id": user_id,
        "created_at": {
            "$gte": today_start
        }
    })

    monthly_count = ai_requests_collection.count_documents({
        "user_id": user_id,
        "created_at": {
            "$gte": month_start
        }
    })

    daily_tokens_result = list(
        ai_requests_collection.aggregate([
            {
                "$match": {
                    "user_id": user_id,
                    "created_at": {
                        "$gte": today_start
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {
                        "$sum": "$tokens_used"
                    }
                }
            }
        ])
    )

    monthly_tokens_result = list(
        ai_requests_collection.aggregate([
            {
                "$match": {
                    "user_id": user_id,
                    "created_at": {
                        "$gte": month_start
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {
                        "$sum": "$tokens_used"
                    }
                }
            }
        ])
    )

    daily_tokens = (
        daily_tokens_result[0]["total"]
        if daily_tokens_result
        else 0
    )

    monthly_tokens = (
        monthly_tokens_result[0]["total"]
        if monthly_tokens_result
        else 0
    )

    subscription = subscriptions_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    daily_limit = None
    remaining_requests = None
    plan_name = None

    if subscription:

        plan_name = subscription.get("plan_name")

        try:
            plan_id = ObjectId(
                subscription["plan_id"]
            )

            plan = plans_collection.find_one({
                "_id": plan_id,
                "status": "active"
            })

            if plan:
                daily_limit = plan.get(
                    "daily_request_limit"
                )

        except Exception:
            pass

    if daily_limit is not None:
        remaining_requests = max(
            0,
            daily_limit - daily_count
        )

    return {
        "plan": plan_name,
        "daily_usage": daily_count,
        "daily_limit": daily_limit,
        "remaining_requests": remaining_requests,
        "monthly_usage": monthly_count,
        "daily_tokens_used": daily_tokens,
        "monthly_tokens_used": monthly_tokens
    }