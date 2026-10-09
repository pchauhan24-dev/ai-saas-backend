from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import (
    plans_collection,
    subscriptions_collection
)

from app.models.subscription import (
    create_subscription_document
)

from app.schemas.subscription import (
    SubscriptionCreate
)

from app.utils.dependencies import (
    get_current_user
)


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


# --------------------------------------------------
# SUBSCRIBE TO A PLAN
# --------------------------------------------------

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def subscribe(
    data: SubscriptionCreate,
    current_user=Depends(get_current_user)
):

    try:
        plan_id = ObjectId(data.plan_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid plan ID"
        )

    plan = plans_collection.find_one({
        "_id": plan_id,
        "status": "active"
    })

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    user_id = str(current_user["_id"])

    existing_subscription = subscriptions_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if existing_subscription:
        raise HTTPException(
            status_code=400,
            detail="User already has an active subscription"
        )

    subscription = create_subscription_document(
        user_id=user_id,
        plan_id=str(plan["_id"]),
        plan_name=plan["name"]
    )

    result = subscriptions_collection.insert_one(
        subscription
    )

    return {
        "message": "Subscription created successfully",
        "subscription_id": str(result.inserted_id),
        "plan": plan["name"],
        "status": "active"
    }


# --------------------------------------------------
# GET CURRENT SUBSCRIPTION
# --------------------------------------------------

@router.get("/current")
def get_current_subscription(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    subscription = subscriptions_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription found"
        )

    return {
        "subscription_id": str(subscription["_id"]),
        "plan_id": subscription["plan_id"],
        "plan_name": subscription["plan_name"],
        "status": subscription["status"],
        "started_at": subscription["started_at"],
        "updated_at": subscription["updated_at"]
    }


# --------------------------------------------------
# UPGRADE / DOWNGRADE PLAN
# --------------------------------------------------

@router.put("/change-plan")
def change_plan(
    data: SubscriptionCreate,
    current_user=Depends(get_current_user)
):

    try:
        plan_id = ObjectId(data.plan_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid plan ID"
        )

    plan = plans_collection.find_one({
        "_id": plan_id,
        "status": "active"
    })

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    user_id = str(current_user["_id"])

    subscription = subscriptions_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription found"
        )

    subscriptions_collection.update_one(
        {"_id": subscription["_id"]},
        {
            "$set": {
                "plan_id": str(plan["_id"]),
                "plan_name": plan["name"],
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return {
        "message": "Subscription plan changed successfully",
        "plan": plan["name"]
    }


# --------------------------------------------------
# CANCEL SUBSCRIPTION
# --------------------------------------------------

@router.put("/cancel")
def cancel_subscription(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    subscription = subscriptions_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription found"
        )

    subscriptions_collection.update_one(
        {"_id": subscription["_id"]},
        {
            "$set": {
                "status": "cancelled",
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return {
        "message": "Subscription cancelled successfully"
    }