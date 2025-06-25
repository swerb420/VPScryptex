# Windmill: Main Python Function
# Path: /post_to_buffer.py
# Description: Adds a new post to the Buffer queue for one or more social profiles.
# SETUP:
# 1. Create a Buffer Developer App to get API access.
# 2. Get your Buffer Access Token.
# 3. In Windmill, store the token as a secret (e.g., `BUFFER_ACCESS_TOKEN`).
# 4. You will also need the Profile IDs for the accounts you want to post to.
#    You can get these from the `user.json` endpoint of the Buffer API.

import requests
from typing import List, Dict, Any

# --- Main Function ---
def main(
    buffer_access_token: str, # Secret from Windmill
    profile_ids: List[str],
    post_text: str,
    media_url: str = None, # Optional: URL for an image or video
    post_now: bool = False
) -> Dict[str, Any]:
    """
    Creates a new update in Buffer.

    Args:
        buffer_access_token: Your Buffer API access token.
        profile_ids: A list of Buffer profile IDs to post to.
        post_text: The text content of the social media post.
        media_url: Optional URL of an image or video to attach.
        post_now: If True, post immediately. If False, add to the queue.

    Returns:
        A dictionary containing the API response from Buffer.
    """
    if not profile_ids:
        return {"status": "error", "message": "No profile_ids provided."}

    print(f"Creating Buffer post for {len(profile_ids)} profile(s).")
    
    # --- Step 1: Prepare the API request payload ---
    api_url = "https://api.bufferapp.com/1/updates/create.json"
    
    headers = {
        "Authorization": f"Bearer {buffer_access_token}"
    }
    
    data = {
        "text": post_text,
        "profile_ids[]": profile_ids,
        "now": "true" if post_now else "false",
        "shorten": "false", # Usually better to handle links manually
    }
    
    # Add media if a URL is provided
    if media_url:
        data["media[link]"] = media_url
        data["media[photo]"] = media_url # Often the same for simple images
        
    # --- Step 2: Make the POST request to Buffer's API ---
    try:
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status() # Raise an exception for non-2xx status codes
        
        response_data = response.json()
        
        if response_data.get("success"):
            update_count = len(response_data.get("updates", []))
            print(f"Successfully created {update_count} update(s) in Buffer.")
            return {"status": "success", "response": response_data}
        else:
            # Buffer sometimes returns success=false with details in the message
            error_message = response_data.get("message", "Unknown error from Buffer.")
            print(f"Buffer API returned an error: {error_message}")
            return {"status": "error", "message": error_message, "response": response_data}

    except requests.exceptions.HTTPError as e:
        # Provide more context on HTTP errors
        error_details = e.response.json() if e.response else {}
        print(f"HTTP Error posting to Buffer: {e.response.status_code} - {error_details}")
        return {"status": "error", "message": str(e), "details": error_details}
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
        return {"status": "error", "message": str(e)}

# Example of how this might be called:
# main(
#     buffer_access_token="1/abcd...",
#     profile_ids=["5f8d8c...","5f8d8d..."],
#     post_text="This post was scheduled automatically using Windmill!",
#     media_url="https://windmill.dev/logo.png",
#     post_now=False
# )
