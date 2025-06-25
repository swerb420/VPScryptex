# Windmill: Main Python Function
# Path: /inputs/webhook_trigger.py
# Description: A webhook to receive external triggers (e.g., from a CMS,
# IFTTT, or a new blog post). It takes a raw payload and passes it
# to the main smart_router workflow.

from typing import Dict, Any
import os

# This script would typically use Windmill's `wm_run_script_async`
# to call the router. We'll simulate that logic.

# --- Main Function ---
def main(
    # Windmill automatically passes the request body to the `body` argument
    # for webhooks with the "application/json" content type.
    body: Dict[str, Any]
) -> Dict:
    """
    Receives a webhook payload and triggers the main content workflow.

    Args:
        body: The JSON payload from the incoming webhook request.
              It's expected to contain a "prompt" field.

    Returns:
        A confirmation that the workflow has been triggered.
    """
    print(f"[Webhook Trigger] Received payload: {body}")

    prompt = body.get("prompt")
    if not prompt:
        return {
            "status": "error",
            "message": "Webhook payload must contain a 'prompt' field."
        }

    # In a real Windmill workflow, you would now trigger the main router script.
    # This would look something like:
    #
    # from windmill_api.windmill_api import WindmillApi
    # client = WindmillApi()
    # client.run_script_async(
    #     path="router/smart_router",
    #     args={"user_prompt": prompt}
    # )
    #
    # For this example, we'll just return the action that would be taken.
    
    print(f"[Webhook Trigger] Triggering router with prompt: '{prompt}'")
    
    return {
        "status": "success",
        "message": "Smart router workflow triggered successfully.",
        "triggered_with_prompt": prompt
    }
