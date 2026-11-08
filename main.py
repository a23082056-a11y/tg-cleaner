import asyncio
import os
from aiohttp import web
from pyrogram import Client, filters

# Создаем веб-сервер для Render Web Service
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

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.me & filters.command("del", prefixes="."))
async def clear_chat(client, message):
    chat_id = message.chat.id
    await message.delete()
    
    async for msg in client.get_chat_history(chat_id, limit=100):
        try:
            await client.delete_messages(chat_id, msg.id, revoke=True)
            await asyncio.sleep(0.03)
        except Exception:
            pass

async def main():
    # Явно создаем и устанавливаем event loop для совместимости
    loop = asyncio.get_running_loop()
    asyncio.set_event_loop(loop)
    
    await start_web_server()
    await app.start()
    print("Bot started successfully!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
