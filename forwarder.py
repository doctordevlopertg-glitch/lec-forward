import asyncio
from pyrogram import Client, filters
import os

# ─── CONFIG ─────────────────────────────────────────────────────

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION_STRING", "")

SOURCE_CHATS = [
    int(x.strip())
    for x in os.environ.get("SOURCE_CHATS", "").split(",")
    if x.strip()
]

DEST_CHAT = int(os.environ.get("DEST_CHAT", "0"))

DELAY_SECONDS = 5

# ────────────────────────────────────────────────────────────────

app = Client(
    "forwarder",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)


@app.on_message(filters.channel & filters.chat(SOURCE_CHATS))
async def forward_message(client, message):

    print(f"📥 New message detected: {message.id}")

    await asyncio.sleep(DELAY_SECONDS)

    try:
        # COPY instead of FORWARD
        await message.copy(DEST_CHAT)

        print(f"✅ Copied msg {message.id}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 Heroku forwarder running...")
    app.run()
