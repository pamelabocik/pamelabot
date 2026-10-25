import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ChatJoinRequest

BOT_TOKEN = "8953794690:AAFORDporaYIYKCOYLudHLlu-IhUFSUX8To"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.chat_join_request()
async def approve(update: ChatJoinRequest):
    await update.approve()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
