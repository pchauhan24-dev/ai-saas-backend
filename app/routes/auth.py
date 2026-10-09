from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.database import users_collection
from app.models.user import create_user_document
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    ProfileResponse
)
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token
)
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest):

    # Do not allow users to create admin accounts
    if data.role not in ["user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )

    existing_user = users_collection.find_one({
        "email": data.email
    })

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(data.password)

    user_document = create_user_document(
        name=data.name,
        email=data.email,
        password=hashed_password,
        role="user"
    )

    result = users_collection.insert_one(user_document)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "role": "user"
    }


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):

    user = users_collection.find_one({
        "email": data.email
    })

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if user.get("status") != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is blocked"
        )

    access_token = create_access_token(
        str(user["_id"]),
        user["role"]
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/profile", response_model=ProfileResponse)
def get_profile(
    current_user=Depends(get_current_user)
):

    return {
        "message": "Profile retrieved successfully",
        "user": {
            "id": str(current_user["_id"]),
            "name": current_user["name"],
            "email": current_user["email"],
            "role": current_user["role"],
            "status": current_user["status"]
        }
    }


@router.post("/logout")
def logout(
    current_user=Depends(get_current_user)
):

    return {
        "message": "Logout successful. Please remove the token from the client."
    }