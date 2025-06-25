# /outputs/create_draft_post.py

import json
from datetime import datetime, timedelta
from typing import Dict, Any

# This script simulates saving a draft to a "database" or "CMS".
# In a real system, this might interact with a specific API (e.g., a headless CMS
# like Contentful, or even a simple database like Firestore or a shared file system).
# For this example, we'll just format the data and return it.

def w_main(
    video_generation_output: Dict[str, Any],
    script_text: str,
    idea_details: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Takes the final generated assets and compiles them into a draft post.

    Args:
        video_generation_output: The output from /engines/generate_video.py.
        script_text: The original text script used for the video.
        idea_details: The specific idea object from the ideation script.

    Returns:
        A dictionary representing the draft post, ready for approval.
    """
    print("Creating draft post from generated assets...")

    if video_generation_output.get("status") != "completed":
        return {"status": "error", "message": "Video generation was not completed successfully."}

    try:
        draft = {
            "draft_id": f"draft_{int(datetime.now().timestamp())}",
            "status": "pending_approval",
            "created_at": datetime.utcnow().isoformat(),
            "title": idea_details.get("title", "Untitled Post"),
            "description": f"Concept: {idea_details.get('concept', '')}\n\n---\nScript:\n{script_text}",
            "platforms": ["youtube", "tiktok"], # Example target platforms
            "assets": {
                "video_url": video_generation_output.get("url"),
                "thumbnail_url": video_generation_output.get("thumbnail_url"),
            },
            "source_idea": idea_details,
            "metadata": video_generation_output,
        }
        print(f"Successfully created draft with ID: {draft['draft_id']}")
        return {"status": "success", "draft": draft}

    except Exception as e:
        message = f"An error occurred while creating the draft: {e}"
        print(message)
        return {"status": "error", "message": message}

# Example Usage
if __name__ == "__main__":
    mock_video_output = {
        "status": "completed",
        "job_id": "job_12345",
        "url": "https://mock-video-generator.com/v/xyz123.mp4",
        "thumbnail_url": "https://mock-video-generator.com/t/xyz123.jpg",
        "duration": 58,
    }
    mock_script = "This is the final script for the video. It's about AI taking over."
    mock_idea = {
        "title": "AI Just Changed Everything... Again",
        "concept": "A quick look at the newest AI model and its shocking capabilities.",
        "hook": "You won't believe what AI can do now."
    }

    draft_post = w_main(mock_video_output, mock_script, mock_idea)
    print("\n--- Final Result ---")
    print(json.dumps(draft_post, indent=2))


