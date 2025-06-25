"""
Handles Telegram commands to manage tracked wallets for monitoring.
Commands: /addwallet, /removewallet, /wallets, /balance
"""
import os
import json
import aiohttp
import asyncio
from aiohttp import web

BOT_TOKEN = os.getenv("WALLET_TELEGRAM_TOKEN")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
WALLET_DB = "tracked_wallets.json"

async def load_wallets():
    if os.path.exists(WALLET_DB):
        with open(WALLET_DB, 'r') as f:
            return json.load(f)
    return []

async def save_wallets(wallets):
    with open(WALLET_DB, 'w') as f:
        json.dump(wallets, f, indent=2)

async def get_balance(address: str) -> float:
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data.get("status") != "1":
                return -1
            return int(data["result"]) / 1e18

async def handle_telegram_command(request):
    body = await request.json()
    message = body.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id or not text:
        return web.Response(text="Ignored")

    response_text = ""
    wallets = await load_wallets()
    args = text.split()

    if text.startswith("/addwallet") and len(args) == 2:
        new_wallet = args[1]
        if new_wallet not in wallets:
            wallets.append(new_wallet)
            await save_wallets(wallets)
            response_text = f"✅ Wallet added: `{new_wallet}`"
        else:
            response_text = "⚠️ Wallet already tracked."

    elif text.startswith("/removewallet") and len(args) == 2:
        wallet = args[1]
        if wallet in wallets:
            wallets.remove(wallet)
            await save_wallets(wallets)
            response_text = f"🗑️ Wallet removed: `{wallet}`"
        else:
            response_text = "⚠️ Wallet not found."

    elif text.startswith("/wallets"):
        if wallets:
            response_text = "📋 Tracked wallets:\n" + "\n".join(wallets)
        else:
            response_text = "📭 No wallets currently tracked."

    elif text.startswith("/balance") and len(args) == 2:
        balance = await get_balance(args[1])
        if balance >= 0:
            response_text = f"💰 Balance for `{args[1]}`: {balance:.4f} ETH"
        else:
            response_text = "⚠️ Error fetching balance."
    else:
        response_text = "Unknown command. Try /addwallet or /wallets."

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    async with aiohttp.ClientSession() as session:
        await session.post(send_url, json={
            "chat_id": chat_id,
            "text": response_text,
            "parse_mode": "Markdown"
        })

    return web.Response(text="OK")

app = web.Application()
app.router.add_post("/wallet-command", handle_telegram_command)

if __name__ == "__main__":
    web.run_app(app, port=9001)