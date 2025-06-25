# Windmill: Main Python Function
# Path: /engines/generate_news_commentary.py
# Description: Fetches content from a URL or searches a topic, then
# uses an LLM to generate commentary.

import requests
import json
from typing import Dict

# Assume a simple web scraper or a search API. For this example, we'll
# just use a placeholder for fetching content. For a real implementation,
# libraries like `beautifulsoup4` or a proper search API would be used.

# --- Main Function ---
def main(
    topic: str = None,
    article_url: str = None,
    generation_model: str = "claude-3-opus-20240229", # From config
    system_prompt: str = "You are a news analyst.", # From config
    anthropic_api_key: str = None # Secret
) -> Dict:
    """
    Generates commentary on a news topic or article.

    Args:
        topic: A topic to search for news on.
        article_url: A specific URL to analyze.
        generation_model: The LLM to use for commentary.
        system_prompt: The persona for the LLM.
        anthropic_api_key: API key for the generation model.

    Returns:
        A dictionary with the source and the commentary.
    """
    if not topic and not article_url:
        return {"status": "error", "message": "Either topic or article_url must be provided."}

    print(f"[News Engine] Task received. Topic: {topic}, URL: {article_url}")

    # --- Step 1: Get Article Content ---
    if article_url:
        # In a real scenario, you'd use a robust scraper.
        article_content = f"Content from {article_url}: [Placeholder - in a real script, this would be scraped text]."
        source_display = article_url
    else:
        # Placeholder for a search API like Perplexity or Google Search.
        article_content = f"Top search result for '{topic}': [Placeholder - this would be search result text]."
        source_display = f"Search results for '{topic}'"

    # --- Step 2: Generate Commentary ---
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=anthropic_api_key)

        user_prompt = f"Based on the following content, please generate commentary as instructed.\n\n**Article Content:**\n{article_content}"

        message = client.messages.create(
            model=generation_model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        commentary = message.content[0].text
        
        print("[News Engine] Commentary generated successfully.")
        return {
            "status": "success",
            "source": source_display,
            "commentary": commentary,
            "model_used": generation_model
        }

    except Exception as e:
        print(f"[News Engine] Error: {e}")
        return {"status": "error", "message": str(e)}
