import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import ChatJoinRequest

logging.basicConfig(level=logging.INFO)

# 1. TWÓJ TOKEN Z BOTFATHER:
BOT_TOKEN = "8913394119:AAH26k20mnPl-BcRRk2MHh4UuHGj0O5HtTQ"

# 2. TWÓJ LINK DO ZDJĘCIA:
PHOTO_URL = "https://i.postimg.cc/4xcXWvQJ/IMG-8057.jpg"

# 3. TWOJA NOWA WIADOMOŚĆ Z FORMATOWANIEM:
CAPTION_TEXT = """✨ <b><i>Witam na moim kanale! cieszę się że do mnie dołączyłeś i mam nadzieję że zostaniesz ze mną na dłużej!</i></b>

<i>uwielbiam zawierać nowe znajomości, więc jeśli wciąż zastanawiasz się czy do mnie napisać - odpowiedź brzmi TAK!❤️</i>

✨ <b><i>dla nowych klientów przygotowane mam duże, specjalne rabaty oraz niespodzianki!</i></b>

🤍 kliknij w moją nazwę użytkownika i napisz do mnie 
👉🏼 <b>@twojapamelcia</b>

lub kliknij w poniższe okno czatu: https://t.me/twojapamelcia"""

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

    # Krok 2: Wysłanie prywatnej wiadomości ze zdjęciem i formatowaniem HTML
    try:
        await bot.send_photo(
            chat_id=event.from_user.id,
            photo=PHOTO_URL,
            caption=CAPTION_TEXT,
            parse_mode="HTML"
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
