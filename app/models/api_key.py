from datetime import datetime, timezone
import secrets


def generate_api_key():
    return "sk-" + secrets.token_urlsafe(32)


def create_api_key_document(user_id: str):
    return {
        "user_id": user_id,
        "api_key": generate_api_key(),
        "status": "active",
        "created_at": datetime.now(timezone.utc),
        "last_used_at": None,
        "usage_count": 0
    }