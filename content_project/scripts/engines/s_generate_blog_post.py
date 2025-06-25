# /engines/generate_blog_post.py

import os
import json
import requests
from typing import Dict, Any

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

def write_article(idea: Dict[str, Any]) -> Dict[str, Any]:
    """Uses Gemini to write a full blog post based on a content idea."""
    print(f"Generating blog post for title: '{idea.get('title')}'")

    prompt = f"""
    You are a skilled content writer and SEO expert specializing in technology and AI.
    Your task is to write an engaging, well-structured, and informative blog post based on the provided idea.

    The blog post should be at least 500 words long and include:
    - An engaging introduction that uses the provided "hook".
    - A main body with several subheadings (using markdown ##).
    - A concluding paragraph that summarizes the key points.
    - SEO-friendly language related to the topic.

    **Content Idea:**
    - **Title:** {idea.get('title')}
    - **Concept:** {idea.get('concept')}
    - **Hook:** {idea.get('hook')}

    Now, write the complete blog post in Markdown format.
    """

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        article_markdown = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        return {
            "status": "success",
            "title": idea.get('title'),
            "article_markdown": article_markdown
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to generate blog post: {e}"}

def w_main(idea: Dict[str, Any]) -> Dict[str, Any]:
    """Windmill entry point."""
    if not all(k in idea for k in ['title', 'concept', 'hook']):
        return {"status": "error", "message": "Idea must contain 'title', 'concept', and 'hook'."}
    
    return write_article(idea)

if __name__ == '__main__':
    mock_idea = {
        "title": "How AI is Learning to See the World in 3D",
        "concept": "Explore the new NeRF technology that lets AI create 3D scenes from 2D images, and what it means for movies, gaming, and the metaverse.",
        "hook": "What if you could turn your phone's photos into a fully explorable 3D world? It's not science fiction anymore."
    }
    
    if not GEMINI_API_KEY:
        print("Skipping __main__ test: GEMINI_API_KEY not set.")
    else:
        blog_post = w_main(mock_idea)
        print(json.dumps(blog_post, indent=2))
        # To see the formatted article:
        # if blog_post.get('status') == 'success':
        #     print("\n--- ARTICLE ---")
        #     print(blog_post['article_markdown'])

