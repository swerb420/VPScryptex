# /outputs/post_to_platforms.py

import time
import json
from typing import Dict, Any

# This script simulates posting to social media APIs.
# Each platform (YouTube, TikTok, Instagram) has its own complex API for uploads.
# This script uses mock functions to represent those interactions.

def post_to_youtube(draft: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates uploading a video to YouTube."""
    print(f"POSTING to YouTube: '{draft['title']}'")
    print(f"Video URL: {draft['assets']['video_url']}")
    time.sleep(5) # Simulate API call latency
    print("...YouTube post successful.")
    return {"platform": "youtube", "status": "success", "post_id": f"yt_{int(time.time())}"}

def post_to_tiktok(draft: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates uploading a video to TikTok."""
    print(f"POSTING to TikTok: '{draft['title']}'")
    print(f"Video URL: {draft['assets']['video_url']}")
    time.sleep(3) # Simulate API call latency
    print("...TikTok post successful.")
    return {"platform": "tiktok", "status": "success", "post_id": f"tt_{int(time.time())}"}

def w_main(draft: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes an approved draft and posts it to the specified platforms.

    Args:
        draft: The approved draft object.

    Returns:
        A dictionary with the results of the posting operations.
    """
    print(f"Initiating posting for draft ID: {draft.get('draft_id')}")

    if not draft or draft.get('status') == 'pending_approval':
        # This check is important in a real flow.
        return {"status": "error", "message": "Draft is not approved for posting."}

    target_platforms = draft.get("platforms", [])
    results = []

    if "youtube" in target_platforms:
        results.append(post_to_youtube(draft))

    if "tiktok" in target_platforms:
        results.append(post_to_tiktok(draft))

    # After posting, we could log this success to Google Sheets
    # For example, call the /meta/log_to_google_sheets.py script here.
    # log_data = {"event": "CONTENT_POSTED", "draft_id": draft.get('draft_id'), "results": results}
    # call_windmill_script("/meta/log_to_google_sheets", {"log_data": log_data})

    return {
        "status": "success",
        "draft_id": draft.get('draft_id'),
        "posting_results": results
    }

# Example Usage
if __name__ == "__main__":
    mock_approved_draft = {
      "draft_id": "draft_1679900400",
      "status": "approved",
      "title": "AI Just Changed Everything... Again",
      "platforms": ["youtube", "tiktok"],
      "assets": {
          "video_url": "https://mock-video-generator.com/v/xyz123.mp4"
      }
    }

    final_result = w_main(mock_approved_draft)
    print("\n--- Final Result ---")
    print(json.dumps(final_result, indent=2))

