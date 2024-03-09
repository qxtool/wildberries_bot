import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler
from aiogram_dialog import setup_dialogs
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.callbacks.handlers import callback_router
from bot.dialogs.dialogs import dialog
from bot.handlers.menu_handlers import menu_router
from bot.handlers.other import other_router
from bot.handlers.product_info_handlers import product_router
from bot.handlers.subscription_handlers import subscription_router
from bot.utils.subscriptions import send_subscriptions
from config import settings

# from apscheduler.jobstores.redis import RedisJobStore - Good practice

storage = RedisStorage.from_url(settings.REDIS_URL)
storage.key_builder = DefaultKeyBuilder(with_destiny=True)
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(storage=storage)

scheduler = AsyncIOScheduler(timezone=settings.TIME_ZONE)
scheduler.add_job(
    send_subscriptions, trigger="interval", minutes=5, kwargs={"bot": bot}
)


async def on_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(settings.WEBHOOK_URL)
    scheduler.start()


async def on_shutdown():
    scheduler.remove_all_jobs()
    scheduler.shutdown()
    logging.info("Bot disabled")


def include_all_routers():
    dp.include_router(menu_router)
    dp.include_router(product_router)
    dp.include_router(subscription_router)
    dp.include_router(callback_router)
    dp.include_router(other_router)
    dp.include_router(dialog)
    setup_dialogs(dp)


def main():
    include_all_routers()

    if settings.DEBUG:
        logging.basicConfig(
            format=f"%(asctime)s - %(levelname)s: %(message)s in %(module)s - %(funcName)s - %(lineno)d",
            level=logging.INFO,
        )
    else:
        logging.basicConfig(
            format=f"%(asctime)s - %(levelname)s: %(message)s in %(module)s - %(funcName)s - %(lineno)d",
            level=logging.ERROR,
            handlers=[logging.FileHandler(f"{settings.BASE_DIR}/logs/errors.log")],
        )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
