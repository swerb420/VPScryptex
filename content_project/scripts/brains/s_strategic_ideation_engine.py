import os, json
from openai import OpenAI
from typing import Dict, Any, List

def main(trends_data: Dict = {}, rss_headlines: List[str] = []) -> List[Dict[str, Any]]:
    print("INFO: [Content-Brain] Starting strategic ideation...")
    openai_key = os.environ.get("WMILL_SECRET_OPENAI_API_KEY")
    if not openai_key: raise ValueError("Secret 'OPENAI_API_KEY' is missing.")

    client = OpenAI(api_key=openai_key)

    system_prompt = """
    You are a world-class content strategist for a tech-focused brand. Your job is to analyze raw trend data and news headlines to generate 3 distinct, high-potential content ideas. For each idea, you MUST provide a catchy 'title', a one-sentence 'summary', and the suggested 'format' which must be either exactly 'blog_post' or 'video_script'. Your entire output MUST be a valid JSON object with a single key "ideas" which contains a list of these idea objects.
    """
    user_prompt = f"Use the following intelligence to generate ideas. Google Trends Data: {json.dumps(trends_data)}. Recent News Headlines: {json.dumps(rss_headlines)}"

    try:
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role':'system', 'content':system_prompt}, {'role':'user', 'content':user_prompt}],
            response_format={"type": "json_object"}
        )
        ideas = json.loads(response.choices[0].message.content).get("ideas", [])
        print(f"INFO: [Content-Brain] Generated {len(ideas)} new content ideas.")
        return ideas
    except Exception as e:
        print(f"ERROR: [Content-Brain] Failed to generate ideas. Error: {e}")
        return []