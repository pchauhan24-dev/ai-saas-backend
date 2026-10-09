from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.database import (
    users_collection,
    plans_collection,
    ai_tools_collection,
    ai_requests_collection,
    api_keys_collection,
    subscriptions_collection
)

from app.utils.dependencies import require_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin Panel"]
)


# ==================================================
# USERS
# ==================================================

@router.get("/users")
def get_all_users(
    current_admin=Depends(require_admin)
):
    users = list(users_collection.find())

    response = []

    for user in users:
        response.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "status": user["status"],
            "created_at": user.get("created_at")
        })

    return {
        "count": len(response),
        "users": response
    }


# ==================================================
# BLOCK USER
# ==================================================

@router.put("/users/{user_id}/block")
def block_user(
    user_id: str,
    current_admin=Depends(require_admin)
):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    user = users_collection.find_one({
        "_id": object_id
    })

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.get("role") == "admin":
        raise HTTPException(
            status_code=400,
            detail="Admin users cannot be blocked"
        )

    users_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": "blocked"}}
    )

    return {
        "message": "User blocked successfully"
    }


# ==================================================
# UNBLOCK USER
# ==================================================

@router.put("/users/{user_id}/unblock")
def unblock_user(
    user_id: str,
    current_admin=Depends(require_admin)
):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    user = users_collection.find_one({
        "_id": object_id
    })

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    users_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": "active"}}
    )

    return {
        "message": "User unblocked successfully"
    }


# ==================================================
# PLANS
# ==================================================

@router.get("/plans")
def get_all_plans(
    current_admin=Depends(require_admin)
):
    plans = list(plans_collection.find())

    response = []

    for plan in plans:
        response.append({
            "id": str(plan["_id"]),
            "name": plan["name"],
            "monthly_price": plan["monthly_price"],
            "daily_request_limit": plan["daily_request_limit"],
            "available_ai_models": plan["available_ai_models"],
            "file_upload_limit": plan["file_upload_limit"],
            "features": plan["features"],
            "status": plan["status"]
        })

    return {
        "count": len(response),
        "plans": response
    }


# ==================================================
# AI TOOLS
# ==================================================

@router.get("/ai-tools")
def get_all_ai_tools(
    current_admin=Depends(require_admin)
):
    tools = list(ai_tools_collection.find())

    response = []

    for tool in tools:
        response.append({
            "id": str(tool["_id"]),
            "name": tool["name"],
            "description": tool["description"],
            "required_plans": tool["required_plans"],
            "status": tool["status"]
        })

    return {
        "count": len(response),
        "tools": response
    }


# ==================================================
# AI USAGE ANALYTICS
# ==================================================

@router.get("/usage")
def get_usage_analytics(
    current_admin=Depends(require_admin)
):
    total_requests = ai_requests_collection.count_documents({})

    total_users = users_collection.count_documents({})

    total_tokens_result = list(
        ai_requests_collection.aggregate([
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

    total_tokens = (
        total_tokens_result[0]["total"]
        if total_tokens_result
        else 0
    )

    tool_usage = list(
        ai_requests_collection.aggregate([
            {
                "$group": {
                    "_id": "$tool_name",
                    "requests": {
                        "$sum": 1
                    },
                    "tokens": {
                        "$sum": "$tokens_used"
                    }
                }
            },
            {
                "$sort": {
                    "requests": -1
                }
            }
        ])
    )

    tools = []

    for item in tool_usage:
        tools.append({
            "tool": item["_id"],
            "requests": item["requests"],
            "tokens": item["tokens"]
        })

    return {
        "total_users": total_users,
        "total_ai_requests": total_requests,
        "total_tokens_used": total_tokens,
        "tool_usage": tools
    }


# ==================================================
# API USAGE
# ==================================================

@router.get("/api-usage")
def get_api_usage(
    current_admin=Depends(require_admin)
):
    api_keys = list(api_keys_collection.find())

    total_keys = len(api_keys)

    active_keys = api_keys_collection.count_documents({
        "status": "active"
    })

    total_api_usage_result = list(
        api_keys_collection.aggregate([
            {
                "$group": {
                    "_id": None,
                    "total": {
                        "$sum": "$usage_count"
                    }
                }
            }
        ])
    )

    total_api_usage = (
        total_api_usage_result[0]["total"]
        if total_api_usage_result
        else 0
    )

    return {
        "total_api_keys": total_keys,
        "active_api_keys": active_keys,
        "total_api_usage": total_api_usage
    }


# ==================================================
# SUBSCRIPTIONS
# ==================================================

@router.get("/subscriptions")
def get_all_subscriptions(
    current_admin=Depends(require_admin)
):
    subscriptions = list(
        subscriptions_collection.find()
    )

    response = []

    for subscription in subscriptions:
        response.append({
            "id": str(subscription["_id"]),
            "user_id": subscription["user_id"],
            "plan_id": subscription["plan_id"],
            "plan_name": subscription["plan_name"],
            "status": subscription["status"],
            "started_at": subscription["started_at"],
            "updated_at": subscription["updated_at"]
        })

    return {
        "count": len(response),
        "subscriptions": response
    }