from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.database import api_keys_collection
from app.models.api_key import (
    create_api_key_document,
    generate_api_key
)
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/api-keys",
    tags=["API Key Management"]
)


# --------------------------------------------------
# GENERATE API KEY
# --------------------------------------------------

@router.post("/")
def generate_api_key_for_user(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    existing_key = api_keys_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if existing_key:
        raise HTTPException(
            status_code=400,
            detail="Active API key already exists"
        )

    api_key_document = create_api_key_document(
        user_id=user_id
    )

    api_keys_collection.insert_one(
        api_key_document
    )

    return {
        "message": "API key generated successfully",
        "api_key": api_key_document["api_key"]
    }


# --------------------------------------------------
# GET CURRENT API KEY
# --------------------------------------------------

@router.get("/")
def get_api_key(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    api_key = api_keys_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if not api_key:
        raise HTTPException(
            status_code=404,
            detail="No active API key found"
        )

    return {
        "api_key": api_key["api_key"],
        "status": api_key["status"],
        "created_at": api_key["created_at"],
        "last_used_at": api_key["last_used_at"]
    }


# --------------------------------------------------
# REGENERATE API KEY
# --------------------------------------------------

@router.put("/regenerate")
def regenerate_api_key(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    api_key = api_keys_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if not api_key:
        raise HTTPException(
            status_code=404,
            detail="No active API key found"
        )

    new_key = generate_api_key()

    api_keys_collection.update_one(
        {"_id": api_key["_id"]},
        {
            "$set": {
                "api_key": new_key,
                "created_at": datetime.now(timezone.utc),
                "last_used_at": None,
                "usage_count": 0
            }
        }
    )

    return {
        "message": "API key regenerated successfully",
        "api_key": new_key
    }


# --------------------------------------------------
# DELETE API KEY
# --------------------------------------------------

@router.delete("/")
def delete_api_key(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    api_key = api_keys_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if not api_key:
        raise HTTPException(
            status_code=404,
            detail="No active API key found"
        )

    api_keys_collection.update_one(
        {"_id": api_key["_id"]},
        {
            "$set": {
                "status": "deleted",
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return {
        "message": "API key deleted successfully"
    }


# --------------------------------------------------
# VIEW API USAGE
# --------------------------------------------------

@router.get("/usage")
def get_api_key_usage(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    api_key = api_keys_collection.find_one({
        "user_id": user_id,
        "status": "active"
    })

    if not api_key:
        raise HTTPException(
            status_code=404,
            detail="No active API key found"
        )

    return {
        "api_key": api_key["api_key"],
        "status": api_key["status"],
        "usage_count": api_key.get(
            "usage_count",
            0
        ),
        "created_at": api_key["created_at"],
        "last_used_at": api_key.get(
            "last_used_at"
        )
    }