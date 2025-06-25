# Windmill: Main Python Function
# Path: /post_to_telegram.py
# Description: Posts a message to a specific Telegram chat or channel.
# SETUP:
# 1. Create a Telegram Bot with @BotFather and get the API token.
# 2. Add the bot to your channel or group.
# 3. Find your chat ID. For a public channel, it's `@channelname`. For a
#    private chat, you may need a tool like @userinfobot.

import requests
from typing import Dict, Any

# This script uses the simple `requests` library to avoid a large dependency
# for a simple API call. `python-telegram-bot` is also a great choice.

# --- Main Function ---
def main(
    bot_token: str, # Secret from Windmill
    chat_id: str,   # e.g., "@mychannel" or a numeric ID like "-100123456789"
    message_text: str,
    photo_url: str = None # Optional URL of an image to send
) -> Dict[str, Any]:
    """
    Posts a message and optionally an image to a Telegram chat.

    Args:
        bot_token: The API token for your Telegram bot.
        chat_id: The unique identifier for the target chat.
        message_text: The text message to send. Supports Markdown.
        photo_url: An optional URL of a photo to send with the message.

    Returns:
        A dictionary with the result from the Telegram API.
    """
    print(f"Sending message to Telegram chat: {chat_id}")

    # Use the appropriate API endpoint based on whether a photo is provided
    if photo_url:
        api_method = "sendPhoto"
        payload = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": message_text,
            "parse_mode": "Markdown"
        }
    else:
        api_method = "sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
    
    url = f"https://api.telegram.org/bot{bot_token}/{api_method}"
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        response_data = response.json()
        if response_data.get("ok"):
            print("Message posted successfully to Telegram.")
            return {"status": "success", "response": response_data}
        else:
            print(f"Telegram API returned an error: {response_data.get('description')}")
            return {"status": "error", "response": response_data}

    except requests.exceptions.RequestException as e:
        print(f"Failed to send request to Telegram API: {e}")
        return {"status": "error", "message": str(e)}

# Example of how this might be called:
# main(
#     bot_token="123456:ABC-DEF1234...",
#     chat_id="@my_test_channel",
#     message_text="*Hello from Windmill!* This is an automated post."
# )
