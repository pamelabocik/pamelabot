import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import ChatJoinRequest

logging.basicConfig(level=logging.INFO)

# TWÓJ TOKEN:
BOT_TOKEN = "8953794690:AAFORDporaYIYKCOYLudHLlu-IhUFSUX8To"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.chat_join_request()
async def auto_approve(event: ChatJoinRequest):
    logging.info(f"Otrzymano prośbę od: {event.from_user.id} ({event.from_user.full_name})")
    try:
        await bot.approve_chat_join_request(
            chat_id=event.chat.id,
            user_id=event.from_user.id
        )
        logging.info("Zatwierdzono pomyślnie!")
    except Exception as err:
        logging.error(f"Błąd zatwierdzania: {err}")

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
    # Usuwamy stary webhook na wypadek gdyby wisiał:
    await bot.delete_webhook(drop_pending_updates=False)
    # Wymuszamy nasłuch na chat_join_request:
    await dp.start_polling(bot, allowed_updates=["chat_join_request", "message"])

if __name__ == "__main__":
    asyncio.run(main())
