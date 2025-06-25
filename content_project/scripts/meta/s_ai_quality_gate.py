# /meta/ai_quality_gate.py

import os
import json
import requests
from typing import Dict, Any

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

def run_quality_check(text_to_review: str, brand_guidelines: str) -> Dict[str, Any]:
    """
    Uses Gemini to perform a quality and brand safety check on generated text.
    """
    print("Running AI Quality & Brand Safety Gate...")

    prompt = f"""
    You are the final quality control arbiter for a media brand. Your job is to
    review a piece of AI-generated text before it goes to a human for approval.

    You must evaluate the text based on our brand guidelines.
    Your response MUST be a valid JSON object with three keys:
    1.  "decision": Either "pass" or "fail".
    2.  "score": An integer from 1-10 on how well it aligns with our brand.
    3.  "reason": A brief, one-sentence explanation for your decision.

    **Our Brand Guidelines:**
    {brand_guidelines}

    **Text to Review:**
    ---
    {text_to_review}
    ---

    Now, provide your JSON evaluation.
    """

    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json"}}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        evaluation = json.loads(result_text)
        print(f"Quality Gate decision: {evaluation.get('decision')}. Reason: {evaluation.get('reason')}")
        return {"status": "success", **evaluation}
    except Exception as e:
        return {"status": "error", "message": f"Failed to run quality gate: {e}"}

def w_main(generated_script: str) -> Dict[str, Any]:
    """Windmill entry point."""
    
    # These guidelines could be loaded from a central config file or Windmill variable
    our_brand_guidelines = """
    - Tone: Enthusiastic, informative, and slightly futuristic. Never cynical or overly technical.
    - Safety: Avoid controversial topics, politics, or making definitive financial predictions.
    - Quality: Must be grammatically correct and engaging. Avoid overly aggressive clickbait.
    - Goal: To make complex AI topics accessible and exciting for a general audience.
    """

    if not generated_script:
        return {"status": "error", "message": "No script provided for review."}

    return run_quality_check(generated_script, our_brand_guidelines)

if __name__ == '__main__':
    mock_script_good = "Check out this incredible new AI! It's changing the game for artists everywhere by generating stunning images from simple text prompts. You won't believe what's possible now!"
    mock_script_bad = "This new AI is going to put everyone out of a job. You need to invest in these 3 stocks right now or you'll be left behind. Don't miss out!"
    
    if not GEMINI_API_KEY:
        print("Skipping __main__ test: GEMINI_API_KEY not set.")
    else:
        print("--- Testing GOOD script ---")
        good_result = w_main(mock_script_good)
        print(json.dumps(good_result, indent=2))
        
        print("\n--- Testing BAD script ---")
        bad_result = w_main(mock_script_bad)
        print(json.dumps(bad_result, indent=2))

