import asyncio

from redis.asyncio.client import Redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.enums import ParseMode
from aiohttp.web_app import Application
from aiogram_i18n import I18nMiddleware
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import web
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from .settings import Settings
from .handlers import setup_routers
from .middlewares import setup_middlewares

async def on_startup(
    dispatcher: Dispatcher,
    settings: Settings,
    redis: Redis, 
    bot: Bot
) -> None:
    if settings.webhook:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(
            url=settings.webhook_url.get_secret_value(),
            secret_token=settings.webhook_secret_token.get_secret_value(),
            allowed_updates=dispatcher.resolve_used_update_types()
        )

    i18n_middleware: I18nMiddleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="app/bot/locales"
        )
    )

    setup_routers(dispatcher=dispatcher)
    setup_middlewares(
        dispatcher=dispatcher,
        redis=redis,
        bot=bot,
        settings=settings
    )

    i18n_middleware.setup(dispatcher=dispatcher)


async def main() -> None:
    settings: Settings = Settings()
    bot: Bot = Bot(
        token=settings.bot_token.get_secret_value(), 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    redis_storage: RedisStorage = RedisStorage(
        redis=await settings.redis_dsn(),
        key_builder=DefaultKeyBuilder(
            with_bot_id=True,
            with_destiny=True
        )
    )

    dispatcher: Dispatcher = Dispatcher(
        bot=bot,
        storage=redis_storage,
        settings=settings,
        redis=redis_storage.redis
    )
    dispatcher.startup.register(on_startup)

    if not settings.dev:
        app: Application = web.Application()

        SimpleRequestHandler(
            dispatcher=dispatcher,
            bot=bot,
            secret_token=settings.webhook_secret_token.get_secret_value()
        ).register(app, "/webhook")

        setup_application(app, dispatcher, bot=bot)
        web.run_app(app, host="127.0.0.1", port=8080)

    await dispatcher.start_polling(
        bot,
        allowed_updates=dispatcher.resolve_used_update_types(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")