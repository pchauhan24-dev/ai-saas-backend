from datetime import datetime, timezone


def create_ai_request_document(
    user_id: str,
    tool_id: str,
    tool_name: str,
    prompt: str,
    response: str,
    tokens_used: int
):
    return {
        "user_id": user_id,
        "tool_id": tool_id,
        "tool_name": tool_name,
        "prompt": prompt,
        "response": response,
        "tokens_used": tokens_used,
        "favorite": False,
        "created_at": datetime.now(timezone.utc)
    }