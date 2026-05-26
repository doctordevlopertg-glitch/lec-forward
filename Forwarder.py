import asyncio
from pyrogram import Client, filters
import os

# ─── CONFIG (use environment variables for Heroku) ────────────────────────────
API_ID   = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION  = os.environ.get("SESSION_STRING", "")   # Pyrogram string session

# Source and destination chat IDs (set as env vars, comma-separated for multiple)
SOURCE_CHATS  = [int(x) for x in os.environ.get("SOURCE_CHATS", "0").split(",")]
DEST_CHAT     = int(os.environ.get("DEST_CHAT", "0"))

DELAY_SECONDS = 5
# ──────────────────────────────────────────────────────────────────────────────

app = Client(
    "forwarder",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION   # string session — no file needed on Heroku
)


@app.on_message(filters.chat(SOURCE_CHATS))
async def forward_message(client, message):
    await asyncio.sleep(DELAY_SECONDS)
    try:
        await message.forward(DEST_CHAT)
        print(f"✅ Forwarded msg {message.id} after {DELAY_SECONDS}s delay")
    except Exception as e:
        print(f"❌ Error forwarding msg {message.id}: {e}")


if __name__ == "__main__":
    print("🚀 Heroku forwarder running...")
    app.run()
