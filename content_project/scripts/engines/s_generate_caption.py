# Windmill: Main Python Function
# Path: /engines/generate_caption.py
# Description: Generates a social media caption using a specified LLM.
# It takes structured input from the smart_router and config.

import json
from openai import OpenAI # Assuming OpenAI for this example
# Add other clients like `anthropic` or `google.generativeai` as needed.

# --- Main Function ---
def main(
    topic: str,
    tone: str,
    platform: str,
    model: str, # e.g., "gpt-4-turbo" from config
    system_prompt: str, # The persona/base instruction from config
    openai_api_key: str, # Injected as a secret
    hashtag_count: int = 5,
    include_emojis: bool = True,
) -> dict:
    """
    Generates a social media caption.
    
    Args:
        topic: The subject of the caption.
        tone: The desired tone of voice.
        platform: The target social media platform.
        model: The specific LLM to use.
        system_prompt: A base prompt defining the AI's persona.
        openai_api_key: The API key for the LLM provider.
        hashtag_count: Number of hashtags to generate.
        include_emojis: Whether to include emojis.
        
    Returns:
        A dictionary with the generated caption and hashtags.
    """
    print(f"[Caption Engine] Generating caption for topic: {topic}")
    
    client = OpenAI(api_key=openai_api_key)

    platform_constraints = {
        "twitter": "Make it very concise (under 280 chars).",
        "instagram": "Focus on visual language and engagement.",
        "linkedin": "Use a professional, business-oriented tone.",
        "facebook": "Encourage discussion and sharing."
    }
    constraint = platform_constraints.get(platform, "Write a general-purpose caption.")

    user_prompt = f"""
    Please generate a social media post with the following specifications.
    - **Topic:** {topic}
    - **Tone:** {tone}
    - **Platform:** {platform} ({constraint})
    - **Hashtags required:** {hashtag_count}
    - **Include Emojis:** {include_emojis}

    Format your response as a single, valid JSON object with two keys:
    1. "caption_text": The complete caption.
    2. "hashtags": A list of strings, each being a hashtag starting with '#'.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        result = json.loads(content)
        
        print("[Caption Engine] Successfully generated caption.")
        return {
            "status": "success",
            "output": result,
            "model_used": model
        }

    except Exception as e:
        print(f"[Caption Engine] Error: {e}")
        return {"status": "error", "message": str(e)}
