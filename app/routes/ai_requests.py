from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import (
    ai_requests_collection,
    ai_tools_collection,
    subscriptions_collection,
    plans_collection
)

from app.schemas.ai_request import (
    AIRequestCreate,
    FavoriteUpdate
)

from app.models.ai_request import (
    create_ai_request_document
)

from app.utils.dependencies import (
    get_current_user
)

from app.utils.ai_engine import (
    generate_mock_response
)

from app.utils.usage import (
    get_today_start,
    estimate_tokens
)


router = APIRouter(
    prefix="/ai-requests",
    tags=["AI Requests"]
)


# --------------------------------------------------
# SEND AI REQUEST
# --------------------------------------------------

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_ai_request(
    data: AIRequestCreate,
    current_user=Depends(get_current_user)
):

    # Validate tool ID
    try:
        tool_id = ObjectId(data.tool_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid AI tool ID"
        )

    # Find active tool
    tool = ai_tools_collection.find_one({
        "_id": tool_id,
        "status": "active"
    })

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="AI tool not found"
        )

    user_id = str(current_user["_id"])

    # Find user's active subscription
    subscription = subscriptions_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="No active subscription found"
        )

    # Find subscription plan
    try:
        plan_id = ObjectId(subscription["plan_id"])
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Invalid subscription plan"
        )

    plan = plans_collection.find_one({
        "_id": plan_id,
        "status": "active"
    })

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found"
        )

    plan_name = plan["name"]

    # Check tool access
    required_plans = tool.get(
        "required_plans",
        []
    )

    if (
        required_plans
        and plan_name not in required_plans
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                f"AI tool is not available "
                f"for the {plan_name} plan"
            )
        )

    # Check daily request limit
    daily_limit = plan.get(
        "daily_request_limit"
    )

    if daily_limit is not None:

        today_start = get_today_start()

        today_count = ai_requests_collection.count_documents({
            "user_id": user_id,
            "created_at": {
                "$gte": today_start
            }
        })

        if today_count >= daily_limit:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Daily AI request limit reached"
                )
            )

    # Generate mock AI response
    response = generate_mock_response(
        tool["name"],
        data.prompt
    )

    tokens_used = estimate_tokens(
        data.prompt + " " + response
    )

    # Save request
    request_document = create_ai_request_document(
        user_id=user_id,
        tool_id=str(tool["_id"]),
        tool_name=tool["name"],
        prompt=data.prompt,
        response=response,
        tokens_used=tokens_used
    )

    result = ai_requests_collection.insert_one(
        request_document
    )

    return {
        "message": "AI request processed successfully",
        "request_id": str(result.inserted_id),
        "tool": tool["name"],
        "prompt": data.prompt,
        "response": response,
        "tokens_used": tokens_used
    }


# --------------------------------------------------
# VIEW MY REQUEST HISTORY
# --------------------------------------------------

@router.get("/")
def get_my_requests(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    requests = list(
        ai_requests_collection.find({
            "user_id": user_id
        }).sort(
            "created_at",
            -1
        )
    )

    response = []

    for request in requests:
        response.append({
            "id": str(request["_id"]),
            "tool": request["tool_name"],
            "prompt": request["prompt"],
            "response": request["response"],
            "tokens_used": request["tokens_used"],
            "favorite": request.get(
                "favorite",
                False
            ),
            "created_at": request["created_at"]
        })

    return {
        "count": len(response),
        "requests": response
    }


# --------------------------------------------------
# DELETE REQUEST HISTORY
# --------------------------------------------------

@router.delete("/{request_id}")
def delete_request(
    request_id: str,
    current_user=Depends(get_current_user)
):

    try:
        object_id = ObjectId(request_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    user_id = str(current_user["_id"])

    result = ai_requests_collection.delete_one({
        "_id": object_id,
        "user_id": user_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    return {
        "message": "Request history deleted successfully"
    }


# --------------------------------------------------
# MARK / UNMARK FAVORITE
# --------------------------------------------------

@router.put("/{request_id}/favorite")
def update_favorite(
    request_id: str,
    data: FavoriteUpdate,
    current_user=Depends(get_current_user)
):

    try:
        object_id = ObjectId(request_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    user_id = str(current_user["_id"])

    result = ai_requests_collection.update_one(
        {
            "_id": object_id,
            "user_id": user_id
        },
        {
            "$set": {
                "favorite": data.favorite
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    return {
        "message": (
            "Request marked as favorite"
            if data.favorite
            else "Request removed from favorites"
        )
    }