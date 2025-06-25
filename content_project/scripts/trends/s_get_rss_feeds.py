# /trends/rss_watcher.py

import feedparser
import json
from typing import List, Dict, Any
from datetime import datetime, time, timedelta

def get_recent_articles(rss_feed_url: str, hours_ago: int = 24) -> Dict[str, Any]:
    """
    Parses an RSS feed and returns entries published within a given time window.

    Args:
        rss_feed_url: The URL of the RSS feed to parse.
        hours_ago: The lookback window in hours to filter recent articles.

    Returns:
        A dictionary containing a list of recent articles or an error message.
    """
    print(f"Fetching RSS feed: {rss_feed_url}")
    try:
        feed = feedparser.parse(rss_feed_url)

        if feed.bozo:
            # Bozo bit is set if the feed is not well-formed
            raise ValueError(f"Feed parsing error: {feed.bozo_exception}")

        recent_entries = []
        time_threshold = datetime.utcnow() - timedelta(hours=hours_ago)

        for entry in feed.entries:
            published_time = None
            if 'published_parsed' in entry:
                # 'published_parsed' is a time.struct_time object
                published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))

            # If no published time, we can't filter, so we might skip or include
            if published_time and published_time >= time_threshold:
                recent_entries.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", ""),
                    "published_date": published_time.isoformat()
                })

        print(f"Found {len(recent_entries)} new articles in the last {hours_ago} hours.")
        return {
            "status": "success",
            "feed_title": feed.feed.get("title", "Unknown Title"),
            "articles": recent_entries
        }

    except Exception as e:
        error_message = f"An error occurred while fetching or parsing the RSS feed: {e}"
        print(error_message)
        return {"status": "error", "message": error_message}

def w_main(rss_feed_url: str, hours_ago: int = 24) -> Dict[str, Any]:
    """
    Windmill entry point to get recent articles from an RSS feed.

    Args:
        rss_feed_url: The URL of the feed.
        hours_ago: Lookback window.

    Returns:
        A dictionary of recent articles.
    """
    if not rss_feed_url:
        return {"status": "error", "message": "RSS feed URL cannot be empty."}

    return get_recent_articles(rss_feed_url, hours_ago)

# Example Usage
if __name__ == "__main__":
    # To run locally, you need: pip install feedparser
    # Using a common tech news RSS feed for the example
    tech_feed = "http://feeds.arstechnica.com/arstechnica/index"
    
    rss_data = w_main(rss_feed_url=tech_feed, hours_ago=72) # Lookback 3 days for more results
    
    print("\n--- Final Result ---")
    print(json.dumps(rss_data, indent=2))

