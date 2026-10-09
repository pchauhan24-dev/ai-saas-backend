from datetime import datetime, timezone


def create_user_document(
    name: str,
    email: str,
    password: str,
    role: str = "user"
):
    return {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "status": "active",
        "created_at": datetime.now(timezone.utc)
    }