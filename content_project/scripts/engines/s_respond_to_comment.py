# Windmill: Main Python Function
# Path: /engines/respond_to_comments.py
# Description: Generates a reply to a social media comment using Claude.

from typing import Dict
from anthropic import Anthropic

# --- Main Function ---
def main(
    comment_text: str,
    comment_author: str,
    original_post_context: str,
    model: str, # "claude-3-sonnet-20240229" from config
    system_prompt: str, # From config
    anthropic_api_key: str # Secret
) -> Dict:
    """
    Generates a draft reply to a user comment for approval.

    Args:
        comment_text: The user's comment.
        comment_author: The user's username.
        original_post_context: The text of the post they commented on.
        model: The LLM to use for the reply.
        system_prompt: The persona for the AI assistant.
        anthropic_api_key: The API key for Anthropic.

    Returns:
        A dictionary with the suggested reply.
    """
    print(f"[Comment Engine] Generating reply for '{comment_author}'")

    client = Anthropic(api_key=anthropic_api_key)

    user_prompt = f"""
    A user named '{comment_author}' left the following comment on our post.
    
    **Our Original Post's Content:**
    ---
    {original_post_context}
    ---

    **Their Comment:**
    ---
    {comment_text}
    ---
    
    Please draft a reply based on your system instructions.
    """

    try:
        message = client.messages.create(
            model=model,
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        suggested_reply = message.content[0].text
        
        print("[Comment Engine] Successfully generated draft reply.")
        return {
            "status": "success",
            "suggested_reply": suggested_reply,
            "model_used": model
        }
    except Exception as e:
        print(f"[Comment Engine] Error: {e}")
        return {"status": "error", "message": str(e)}
