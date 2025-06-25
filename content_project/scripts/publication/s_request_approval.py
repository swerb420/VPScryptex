# File: s_request_approval.py
# This script sends a message to your content channel asking for approval.
import os
import requests

def main(content_draft: dict) -> dict:
    print("INFO: [Content-Approval] Sending draft for human approval.")

    # --- THIS USES THE CONTENT-SPECIFIC SECRETS ---
    bot_token = os.environ.get("WMILL_SECRET_TELEGRAM_CONTENT_BOT_TOKEN")
    chat_id = os.environ.get("WMILL_SECRET_TELEGRAM_CONTENT_CHAT_ID")
    # ----------------------------------------------

    if not all([bot_token, chat_id]):
        raise ValueError("Content Factory Telegram secrets are missing. Please set them in the Windmill UI.")

    # This is a simplified message. We can make it more advanced with approval buttons later.
    title = content_draft.get('title', 'N/A')
    summary = content_draft.get('summary', 'N/A')

    message = f"✅ **Content Draft Ready for Approval** ✅\n\n" \
              f"**Title:** {title}\n" \
              f"**Summary:** {summary}\n\n" \
              f"Please reply with '/approve' or '/reject'."

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        print("INFO: [Content-Approval] Approval request sent successfully.")
        return {"status": "approval_sent"}
    except Exception as e:
        print(f"ERROR: [Content-Approval] Failed to send approval request. Error: {e}")
        return {"status": "send_failed"}