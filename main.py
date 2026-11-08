import asyncio
import sys

# Жестко создаем цикл событий ДО любых импортов Pyrogram для Python 3.14
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import os
from aiohttp import web
from pyrogram import Client, filters

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app_web = web.Application()
    app_web.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")

API_ID = 31886621
API_HASH = "b2d85f1c4e84f1504a42d7514e23407a"

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.me & filters.command("del", prefixes="."))
async def clear_chat(client, message):
    chat_id = message.chat.id
    try:
        await message.delete()
    except Exception:
        pass
    
    async for msg in client.get_chat_history(chat_id, limit=50):
        try:
            await client.delete_messages(chat_id, msg.id, revoke=True)
            await asyncio.sleep(0.02)
        except Exception:
            break

async def main():
    await start_web_server()
    print("Starting Pyrogram client...")
    await app.start()
    print("Bot started successfully!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop.run_until_complete(main())
