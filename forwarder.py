import asyncio
from pyrogram import Client, filters
import os

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION_STRING"]

SOURCE_CHATS = [
    int(x.strip())
    for x in os.environ["SOURCE_CHATS"].split(",")
]

DEST_CHAT = int(os.environ["DEST_CHAT"])

DELAY_SECONDS = 5

app = Client(
    "forwarder",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

@app.on_message(filters.channel & filters.chat(SOURCE_CHATS))
async def forward_message(client, message):

    print(f"📥 New message: {message.id}")

    await asyncio.sleep(DELAY_SECONDS)

    try:
        await message.copy(DEST_CHAT)

        print(f"✅ Copied: {message.id}")

    except Exception as e:
        print(f"❌ Error: {e}")

print("🚀 Heroku forwarder running...")

app.run()
