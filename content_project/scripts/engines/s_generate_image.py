# Windmill: Main Python Function
# Path: /engines/generate_image.py
# Description: Generates an image using a specified provider (Fal.ai or OpenAI).
# Takes structured input from the smart_router and config.

import requests
from typing import Dict

# --- Main Function ---
def main(
    prompt: str,
    style: str,
    provider: str, # "fal_ai" or "openai" from config
    model: str, # "fal-ai/sdxl" or "dall-e-3" from config
    api_key: str # Secret for the respective provider
) -> Dict:
    """
    Generates an image from a text prompt.

    Args:
        prompt: The main description of the image.
        style: Style keywords (e.g., photorealistic, cartoon).
        provider: The image generation service to use.
        model: The specific model to use.
        api_key: The API key for the chosen provider.

    Returns:
        A dictionary with the URL of the generated image.
    """
    full_prompt = f"{prompt}, {style}"
    print(f"[Image Engine] Provider: {provider}, Prompt: {full_prompt}")

    if provider == "fal_ai":
        return generate_with_fal(full_prompt, model, api_key)
    elif provider == "openai":
        return generate_with_dalle(full_prompt, model, api_key)
    else:
        return {"status": "error", "message": f"Unsupported image provider: {provider}"}

def generate_with_fal(prompt: str, model_path: str, key: str) -> Dict:
    """Handler for Fal.ai image generation."""
    url = f"https://fal.run/{model_path}"
    headers = {"Authorization": f"Key {key}", "Content-Type": "application/json"}
    payload = {"prompt": prompt}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        image_url = data.get("images", [{}])[0].get("url")
        if not image_url:
            raise ValueError("Image URL not found in Fal.ai response.")
        
        print("[Image Engine] Fal.ai image generated successfully.")
        return {"status": "success", "image_url": image_url, "provider": "fal_ai"}
    except Exception as e:
        print(f"[Image Engine] Fal.ai Error: {e}")
        return {"status": "error", "message": str(e)}

def generate_with_dalle(prompt: str, model: str, key: str) -> Dict:
    """Handler for OpenAI DALL-E 3 generation."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        response = client.images.generate(
            model=model,
            prompt=prompt,
            n=1,
            size="1024x1024", # DALL-E 3 supports various sizes
            quality="standard", # or "hd"
        )
        image_url = response.data[0].url
        
        print("[Image Engine] DALL-E 3 image generated successfully.")
        return {"status": "success", "image_url": image_url, "provider": "openai"}
    except Exception as e:
        print(f"[Image Engine] DALL-E 3 Error: {e}")
        return {"status": "error", "message": str(e)}
