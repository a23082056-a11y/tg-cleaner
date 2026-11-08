import asyncio
import os
from pyrogram import Client, filters

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.me & filters.command("del", prefixes="."))
async def clear_chat(client, message):
    chat_id = message.chat.id
    await message.delete()  # Стираем команду .del

    async for msg in client.get_chat_history(chat_id, limit=100):
        try:
            await client.delete_messages(chat_id, msg.id, revoke=True)
            await asyncio.sleep(0.03)
        except Exception:
            pass

app.run()
