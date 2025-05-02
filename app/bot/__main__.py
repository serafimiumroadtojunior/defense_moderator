from typing import Optional
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.enums import ParseMode
from aiohttp.web_app import Application
from aiohttp import web
from fluentogram import TranslatorHub
from dotenv import load_dotenv

from .translation import init_translator_hub
from .handlers import setup_routers
from .middlewares import setup_middlewares
from .config import ENV_FILE

load_dotenv(dotenv_path=ENV_FILE)

async def on_startup(
    dispatcher: Dispatcher, 
    bot: Bot
) -> None:
    webhook_url: Optional[str] = os.getenv("WEBHOOK_URL")
    webhook_secret: Optional[str] = os.getenv("WEBHOOK_SECRET")
    if webhook_url is None or webhook_secret is None:
        raise ValueError("Webhook URL or secret is not set in environment variables")

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=webhook_url,
        secret_token=webhook_secret,
        allowed_updates=dispatcher.resolve_used_update_types()
    )


async def main() -> None:
    token: Optional[str] = os.getenv("TOKEN") 
    webhook_secret: Optional[str] = os.getenv("WEBHOOK_SECRET")
    if token is None:
        raise ValueError("Token is not set in environment variables")
    
    app: Application = web.Application()
    translator_hub: TranslatorHub = init_translator_hub()
    bot: Bot = Bot(
        token=token, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp: Dispatcher = Dispatcher(
        translator_hub=translator_hub,
        bot=bot
    )

    dp.startup.register(on_startup)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=webhook_secret,
    ).register(app, "/webhook")

    setup_application(app, dp, bot=bot)
    setup_middlewares(dispatcher=dp)
    setup_routers(dispatcher=dp)

    web.run_app(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")