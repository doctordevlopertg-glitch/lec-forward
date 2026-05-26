import os
import asyncio
from pyrogram import Client, filters
from pyrogram.idle import idle

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION"]

SOURCE = int(os.environ["SOURCE_CHANNEL"])
DEST = int(os.environ["DEST_CHANNEL"])

app = Client(
    "forwarder",
    api_id=api_id,
    api_hash=api_hash,
    session_string=session
)

queue = asyncio.Queue()

@app.on_message(filters.chat(SOURCE))
async def new_message(_, message):
    await queue.put(message)

async def worker():
    while True:
        message = await queue.get()

        try:
            await message.forward(DEST)
            print(f"Forwarded: {message.id}")

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(5)

async def main():
    await app.start()

    print("Bot Started")

    asyncio.create_task(worker())

    await idle()

    await app.stop()

asyncio.get_event_loop().run_until_complete(main())
