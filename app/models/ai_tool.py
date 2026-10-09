from datetime import datetime, timezone


def create_ai_tool_document(
    name: str,
    description: str,
    required_plans: list[str]
):
    return {
        "name": name,
        "description": description,
        "required_plans": required_plans,
        "status": "active",
        "created_at": datetime.now(timezone.utc)
    }