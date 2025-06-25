import os, requests, json
from typing import Dict, Any

def main(region_code: str = "US", video_category_id: str = "28") -> Dict[str, Any]:
    # 28 = Science & Technology category
    api_key = os.environ.get("WMILL_SECRET_GOOGLE_API_KEY")
    if not api_key: raise ValueError("Secret 'GOOGLE_API_KEY' is missing.")
    
    print(f"INFO: [YouTube Trends] Fetching trending videos for region '{region_code}'.")
    params = {
        "part": "snippet,statistics", "chart": "mostPopular",
        "regionCode": region_code, "videoCategoryId": video_category_id,
        "maxResults": 15, "key": api_key,
    }
    try:
        response = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params)
        response.raise_for_status()
        data = response.json()
        videos = [
            {"title": item["snippet"]["title"], "channel": item["snippet"]["channelTitle"], "views": int(item["statistics"].get("viewCount", 0))}
            for item in data.get("items", [])
        ]
        return {"status": "success", "videos": videos}
    except Exception as e:
        return {"status": "error", "message": str(e)}