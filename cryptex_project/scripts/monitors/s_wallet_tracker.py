"""
Wallet Tracker: Monitors ETH inflow/outflow on tracked wallets.
Controlled via s_wallet_command_bot.py (Telegram commands).
"""

import asyncio
import aiohttp
import os
import time
import logging
import json
from typing import List, Dict

TELEGRAM_TOKEN = os.getenv("WALLET_TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("WALLET_TELEGRAM_CHAT_ID")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
WALLET_DB = "tracked_wallets.json"
CHECK_INTERVAL = 60  # seconds

logging.basicConfig(level=logging.INFO, format='[WALLET TRACKER] %(message)s')


def load_wallets() -> List[str]:
    if os.path.exists(WALLET_DB):
        with open(WALLET_DB, "r") as f:
            return json.load(f)
    return []


async def fetch_wallet_balance(session, wallet: str) -> float:
    url = (
        f"https://api.etherscan.io/api?module=account&action=balance"
        f"&address={wallet}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    )
    async with session.get(url) as resp:
        data = await resp.json()
        if data.get("status") != "1":
            raise Exception(f"Etherscan error: {data.get('message')}")
        return int(data["result"]) / 1e18


async def send_telegram_alert(wallet: str, old_balance: float, new_balance: float):
    direction = "⬆️ IN" if new_balance > old_balance else "⬇️ OUT"
    delta = abs(new_balance - old_balance)
    message = (
        f"{direction} {delta:.4f} ETH\n"
        f"Wallet: `{wallet}`\n"
        f"Old: {old_balance:.4f} | New: {new_balance:.4f}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            result = await resp.json()
            if not result.get("ok"):
                logging.warning(f"Failed to send Telegram alert: {result}")


async def monitor_wallets():
    previous_balances: Dict[str, float] = {}
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                wallets = load_wallets()
                for wallet in wallets:
                    new_balance = await fetch_wallet_balance(session, wallet)
                    old_balance = previous_balances.get(wallet, new_balance)
                    if abs(new_balance - old_balance) > 1.0:  # 1 ETH threshold
                        await send_telegram_alert(wallet, old_balance, new_balance)
                    previous_balances[wallet] = new_balance
                await asyncio.sleep(CHECK_INTERVAL)
            except Exception as e:
                logging.error(f"Monitor error: {e}")
                await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(monitor_wallets())
