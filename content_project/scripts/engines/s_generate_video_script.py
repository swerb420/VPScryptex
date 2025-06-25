# Windmill: Main Python Function
# Path: /engines/generate_video.py
# Description: Initiates a video generation job using a specified provider,
# like Google Cloud Vertex AI. This is an asynchronous operation.

import json
import requests
from typing import Dict

# --- Main Function ---
def main(
    prompt: str,
    provider: str, # e.g., "google_vertex_ai" from config
    model: str,    # e.g., "imagenvideo-001" from config
    gcp_project_id: str,    # Secret
    gcp_access_token: str,  # Secret (short-lived)
    location: str = "us-central1"
) -> Dict:
    """
    Kicks off an asynchronous video generation task.

    Args:
        prompt: The text description for the video.
        provider: The video generation service to use.
        model: The specific video model to use.
        gcp_project_id: Your Google Cloud Project ID.
        gcp_access_token: A valid OAuth2 access token for your GCP account.
        location: The GCP region for the API endpoint.

    Returns:
        A dictionary with the operation details for status checking.
    """
    print(f"[Video Engine] Starting job for prompt: '{prompt}'")

    if provider != "google_vertex_ai":
        return {"status": "error", "message": f"Provider '{provider}' is not supported yet."}
    
    # --- Step 1: Define API Endpoint and Payload for Vertex AI ---
    # This structure is based on Google's standard for long-running AI jobs.
    api_endpoint = f"https://{location}-aiplatform.googleapis.com/v1/projects/{gcp_project_id}/locations/{location}/publishers/google/models/{model}:predict"
    
    headers = {
        "Authorization": f"Bearer {gcp_access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"aspectRatio": "16:9", "fps": 24}
    }

    # --- Step 2: Make the Asynchronous Request ---
    try:
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        operation_data = response.json()
        operation_name = operation_data.get("name")

        if not operation_name:
            raise ValueError("API response did not include an operation name.")

        status_check_url = f"https://{location}-aiplatform.googleapis.com/v1/{operation_name}"
        
        print(f"[Video Engine] Job submitted successfully. Operation: {operation_name}")
        return {
            "status": "submitted",
            "operation_name": operation_name,
            "status_check_url": status_check_url,
            "provider": provider,
            "message": "Video generation started. Poll the status_check_url to get the result."
        }

    except Exception as e:
        print(f"[Video Engine] Error: {e}")
        error_details = {}
        if hasattr(e, 'response') and e.response:
             try:
                error_details = e.response.json()
             except json.JSONDecodeError:
                error_details = {"text": e.response.text}
        return {"status": "error", "message": str(e), "details": error_details}
