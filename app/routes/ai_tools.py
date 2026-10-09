from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import ai_tools_collection
from app.models.ai_tool import create_ai_tool_document
from app.schemas.ai_tool import AIToolCreate, AIToolUpdate
from app.utils.dependencies import get_current_user, require_admin


router = APIRouter(
    prefix="/ai-tools",
    tags=["AI Tools"]
)


# --------------------------------------------------
# GET ALL ACTIVE AI TOOLS
# --------------------------------------------------

@router.get("/")
def get_ai_tools(
    current_user=Depends(get_current_user)
):
    tools = list(
        ai_tools_collection.find(
            {"status": "active"}
        )
    )

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


# --------------------------------------------------
# GET SINGLE AI TOOL
# --------------------------------------------------

@router.get("/{tool_id}")
def get_ai_tool(
    tool_id: str,
    current_user=Depends(get_current_user)
):
    try:
        object_id = ObjectId(tool_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid tool ID"
        )

    tool = ai_tools_collection.find_one({
        "_id": object_id,
        "status": "active"
    })

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="AI tool not found"
        )

    return {
        "id": str(tool["_id"]),
        "name": tool["name"],
        "description": tool["description"],
        "required_plans": tool["required_plans"],
        "status": tool["status"]
    }


# --------------------------------------------------
# ADMIN CREATE AI TOOL
# --------------------------------------------------

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_ai_tool(
    data: AIToolCreate,
    current_admin=Depends(require_admin)
):
    existing_tool = ai_tools_collection.find_one({
        "name": data.name
    })

    if existing_tool:
        raise HTTPException(
            status_code=400,
            detail="AI tool already exists"
        )

    tool_document = create_ai_tool_document(
        name=data.name,
        description=data.description,
        required_plans=data.required_plans
    )

    result = ai_tools_collection.insert_one(
        tool_document
    )

    return {
        "message": "AI tool created successfully",
        "tool_id": str(result.inserted_id)
    }


# --------------------------------------------------
# ADMIN UPDATE AI TOOL
# --------------------------------------------------

@router.put("/{tool_id}")
def update_ai_tool(
    tool_id: str,
    data: AIToolUpdate,
    current_admin=Depends(require_admin)
):
    try:
        object_id = ObjectId(tool_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid tool ID"
        )

    tool = ai_tools_collection.find_one({
        "_id": object_id
    })

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="AI tool not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )

    ai_tools_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    return {
        "message": "AI tool updated successfully"
    }


# --------------------------------------------------
# ADMIN DELETE AI TOOL
# --------------------------------------------------

@router.delete("/{tool_id}")
def delete_ai_tool(
    tool_id: str,
    current_admin=Depends(require_admin)
):
    try:
        object_id = ObjectId(tool_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid tool ID"
        )

    tool = ai_tools_collection.find_one({
        "_id": object_id
    })

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="AI tool not found"
        )

    ai_tools_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": "inactive"}}
    )

    return {
        "message": "AI tool deactivated successfully"
    }