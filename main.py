import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import ChatJoinRequest

logging.basicConfig(level=logging.INFO)

# 1. TWÓJ TOKEN Z BOTFATHER:
BOT_TOKEN = "8953794690:AAFvaYxQnprRo04dFGZ3m9NQBNecxXtm1MI"

# 2. TWÓJ LINK DO ZDJĘCIA:
PHOTO_URL = "https://i.postimg.cc/4xcXWvQJ/IMG-8057.jpg"

# 3. TWOJA WIADOMOŚĆ:
CAPTION_TEXT = """✨ Witam na moim kanale! cieszę się że do mnie dołączyłeś i mam nadzieję że zostaniesz ze mną na dłużej!🤍

Uwielbiam zawierać nowe znajomości więc jeśli wciąż się zastanawiać czy do mnie napisać - odpowiedź brzmi TAK!❤️

kliknij w moją nazwę użytkownika i napisz do mnie✨
👉🏼 @twojapamelcia"""

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.chat_join_request()
async def auto_approve_and_send_message(event: ChatJoinRequest):
    logging.info(f"Otrzymano prośbę od: {event.from_user.id} ({event.from_user.first_name})")
    
    # Krok 1: Akceptacja na kanale
    try:
        await bot.approve_chat_join_request(
            chat_id=event.chat.id,
            user_id=event.from_user.id
        )
        logging.info("Zaakceptowano na kanale!")
    except Exception as err:
        logging.error(f"Błąd akceptacji: {err}")

    # Krok 2: Wysłanie prywatnej wiadomości ze zdjęciem
    try:
        await bot.send_photo(
            chat_id=event.from_user.id,
            photo=PHOTO_URL,
            caption=CAPTION_TEXT
        )
        logging.info("Wiadomość ze zdjęciem wysłana!")
    except Exception as err:
        logging.warning(f"Nie udało się wysłać DM (blokada prywatności użytkownika): {err}")

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
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot, allowed_updates=["chat_join_request", "message"])

if __name__ == "__main__":
    asyncio.run(main())
