from typing import Optional
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.enums import ParseMode
from aiohttp.web_app import Application
from aiohttp import web
from dotenv import load_dotenv

from .handlers import setup_routers
from .middlewares import setup_middlewares

load_dotenv(dotenv_path=os.path.join("defense_moderator", ".env"))

async def on_startup(
    dispatcher: Dispatcher, 
    bot: Bot
) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=os.getenv("WEBHOOK_URL"),
        secret_token=os.getenv("WEBHOOK_SECRET"),
        allowed_updates=dispatcher.resolve_used_update_types()
    )


async def main() -> None:
    token: Optional[str] = os.getenv("TOKEN")  
    if token is None:
        raise ValueError("Token is not set in environment variables")
    
    app: Application = web.Application()
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(
        token=token, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp.startup.register(on_startup)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=os.getenv("WEBHOOK_SECRET")
    ).register(app, "/webhook")

    setup_application(app, dp, bot=bot)
    setup_middlewares(dispatcher=dp, bot=bot)
    setup_routers(dispatcher=dp)

    web.run_app(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")