from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import plans_collection
from app.models.plan import create_plan_document
from app.schemas.plan import PlanCreate, PlanUpdate
from app.utils.dependencies import require_admin


router = APIRouter(
    prefix="/plans",
    tags=["Subscription Plans"]
)


# --------------------------------------------------
# PUBLIC - GET ALL ACTIVE PLANS
# --------------------------------------------------

@router.get("/")
def get_plans():

    plans = list(
        plans_collection.find(
            {"status": "active"}
        )
    )

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


# --------------------------------------------------
# PUBLIC - GET SINGLE PLAN
# --------------------------------------------------

@router.get("/{plan_id}")
def get_plan(plan_id: str):

    try:
        object_id = ObjectId(plan_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid plan ID"
        )

    plan = plans_collection.find_one({
        "_id": object_id,
        "status": "active"
    })

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    return {
        "id": str(plan["_id"]),
        "name": plan["name"],
        "monthly_price": plan["monthly_price"],
        "daily_request_limit": plan["daily_request_limit"],
        "available_ai_models": plan["available_ai_models"],
        "file_upload_limit": plan["file_upload_limit"],
        "features": plan["features"],
        "status": plan["status"]
    }


# --------------------------------------------------
# ADMIN - CREATE PLAN
# --------------------------------------------------

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_plan(
    data: PlanCreate,
    current_admin=Depends(require_admin)
):

    existing_plan = plans_collection.find_one({
        "name": data.name
    })

    if existing_plan:
        raise HTTPException(
            status_code=400,
            detail="Plan already exists"
        )

    plan_document = create_plan_document(
        name=data.name,
        monthly_price=data.monthly_price,
        daily_request_limit=data.daily_request_limit,
        available_ai_models=data.available_ai_models,
        file_upload_limit=data.file_upload_limit,
        features=data.features
    )

    result = plans_collection.insert_one(
        plan_document
    )

    return {
        "message": "Plan created successfully",
        "plan_id": str(result.inserted_id)
    }


# --------------------------------------------------
# ADMIN - UPDATE PLAN
# --------------------------------------------------

@router.put("/{plan_id}")
def update_plan(
    plan_id: str,
    data: PlanUpdate,
    current_admin=Depends(require_admin)
):

    try:
        object_id = ObjectId(plan_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid plan ID"
        )

    plan = plans_collection.find_one({
        "_id": object_id
    })

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )

    plans_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    return {
        "message": "Plan updated successfully"
    }


# --------------------------------------------------
# ADMIN - DELETE / DEACTIVATE PLAN
# --------------------------------------------------

@router.delete("/{plan_id}")
def delete_plan(
    plan_id: str,
    current_admin=Depends(require_admin)
):

    try:
        object_id = ObjectId(plan_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid plan ID"
        )

    plan = plans_collection.find_one({
        "_id": object_id
    })

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    plans_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "status": "inactive"
            }
        }
    )

    return {
        "message": "Plan deactivated successfully"
    }