import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import ChatJoinRequest

BOT_TOKEN = "8953794690:AAFORDporaYIYKCOYLudHLlu-IhUFSUX8To"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.chat_join_request()
async def approve(update: ChatJoinRequest):
    print(f"Otrzymano prosbe od uzytkownika: {update.from_user.id}")
    try:
        await update.approve()
        print("Zaakceptowano pomyslnie!")
    except Exception as e:
        print(f"Blad przy akceptacji: {e}")

async def dummy_web_server():
    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="Bot dziala!"))
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await dummy_web_server()
    # To jest kluczowa zmiana wymuszajaca odbieranie prosb o dolaczenie:
    await dp.start_polling(bot, allowed_updates=["chat_join_request"])

if __name__ == "__main__":
    asyncio.run(main())
