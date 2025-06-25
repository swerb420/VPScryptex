"""
This script takes a list of previously generated content ideas
and repurposes them into different formats (threads, shorts, blog posts).
"""
import os
import json
from openai import OpenAI
from typing import List, Dict

client = OpenAI(api_key=os.getenv("WMILL_SECRET_OPENAI_API_KEY"))

def repurpose_ideas(ideas: List[Dict[str, str]], formats: List[str] = ["twitter_thread", "short_form_video"]) -> List[Dict[str, str]]:
    if not ideas:
        raise ValueError("No ideas provided to repurpose.")

    prompt = f"""
    You are an expert content marketer. Repurpose the following content ideas into different engaging formats.
    For each idea, return a version suitable for each of these formats: {formats}.

    Input:
    {json.dumps(ideas, indent=2)}

    Output as JSON with this schema:
    [
      {
        "original_title": "...",
        "repurposed": {
          "twitter_thread": "...",
          "short_form_video": "..."
        }
      }
    ]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a professional content strategist."},
                {"role": "user", "content": prompt}
            ]
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"[ERROR] Failed to repurpose content: {e}")
        return []

if __name__ == "__main__":
    sample_ideas = [
        {"title": "Why Solana Is Eating Ethereum's Lunch", "summary": "Solana's low fees and fast throughput...", "format": "blog_post"}
    ]
    output = repurpose_ideas(sample_ideas)
    print(json.dumps(output, indent=2))