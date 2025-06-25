# /trends/google_trends_watcher.py

import pandas as pd
from pytrends.request import TrendReq
from typing import List, Dict, Any

# Note: pytrends is an unofficial API for Google Trends.
# Its reliability can vary, and it's important to use it respectfully
# to avoid being rate-limited.

def get_trending_topics(keyword: str = "artificial intelligence", geo: str = 'US') -> Dict[str, Any]:
    """
    Fetches related and rising queries from Google Trends for a given keyword.

    Args:
        keyword: The core topic to search for trends around.
        geo: The geographic region for the trend search (e.g., 'US').

    Returns:
        A dictionary containing lists of top and rising related queries.
        Returns an error message if the operation fails.
    """
    print(f"Fetching Google Trends data for keyword: '{keyword}' in geo: '{geo}'")
    try:
        pytrends = TrendReq(hl='en-US', tz=360) # tz for US Pacific Time

        # Build the payload
        pytrends.build_payload([keyword], cat=0, timeframe='today 1-m', geo=geo, gprop='')

        # Get related queries
        related_queries = pytrends.related_queries()

        rising_queries_df = related_queries.get(keyword, {}).get('rising')
        top_queries_df = related_queries.get(keyword, {}).get('top')

        results = {
            "status": "success",
            "keyword": keyword,
            "rising_queries": rising_queries_df.to_dict('records') if isinstance(rising_queries_df, pd.DataFrame) else [],
            "top_queries": top_queries_df.to_dict('records') if isinstance(top_queries_df, pd.DataFrame) else []
        }
        print("Successfully fetched and processed Google Trends data.")
        return results

    except Exception as e:
        error_message = f"An error occurred while fetching Google Trends data: {e}"
        print(error_message)
        return {"status": "error", "message": error_message}

def w_main(keyword: str, geo: str = 'US') -> Dict[str, Any]:
    """
    Windmill entry point to get trending topics.

    Args:
        keyword: The keyword to search for.
        geo: The two-letter country code.

    Returns:
        The trending topics data.
    """
    if not keyword:
        return {"status": "error", "message": "Keyword cannot be empty."}

    return get_trending_topics(keyword, geo)

# Example Usage:
if __name__ == "__main__":
    # To run this locally, you need: `pip install pytrends`
    trending_data = w_main(keyword="generative art")
    import json
    print("\n--- Final Result ---")
    print(json.dumps(trending_data, indent=2))

