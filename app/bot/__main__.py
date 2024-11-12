import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import setup_routers
from middlewares import setup_middlewares

load_dotenv(dotenv_path=os.path.join("defense_moderator", ".env"))

async def main() -> None:
    TOKEN = os.getenv("TOKEN")  
    if TOKEN is None:
        raise ValueError("Token is not set in environment variables")
    
    bot: Bot = Bot(token=TOKEN)
    dp: Dispatcher = Dispatcher()

    setup_middlewares(dispatcher=dp, bot=bot)
    setup_routers(dispatcher=dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")