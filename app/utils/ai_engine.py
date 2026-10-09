def generate_mock_response(
    tool_name: str,
    prompt: str
) -> str:

    responses = {
        "AI Chat": (
            f"Mock AI Chat Response: "
            f"Here is a helpful response to your prompt: {prompt}"
        ),

        "AI Code Generator": (
            f"Mock AI Code Response: "
            f"Generated code based on your request: {prompt}"
        ),

        "AI Text Summarizer": (
            f"Mock AI Summary: "
            f"The main idea of the provided text is: {prompt}"
        ),

        "AI Image Prompt Generator": (
            f"Mock AI Image Prompt: "
            f"A detailed image generation prompt based on: {prompt}"
        ),

        "AI Email Writer": (
            f"Mock AI Email: "
            f"A professional email based on your request: {prompt}"
        )
    }

    return responses.get(
        tool_name,
        f"Mock AI Response: {prompt}"
    )