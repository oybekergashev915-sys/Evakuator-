import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent

from config import config
from db.models import init_models
from handlers.admin import admin_fallback_router, admin_router
from handlers.client import router as client_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


async def global_error_handler(event: ErrorEvent) -> bool:
    logger.exception("Необработанная ошибка при обработке апдейта", exc_info=event.exception)
    try:
        update = event.update
        if update.message:
            await update.message.answer("⚠️ Произошла непредвиденная ошибка. Попробуйте ещё раз позже.")
        elif update.callback_query:
            await update.callback_query.answer(
                "⚠️ Произошла ошибка. Попробуйте ещё раз.", show_alert=True
            )
    except Exception:
        logger.exception("Не удалось отправить сообщение об ошибке пользователю")
    return True


async def main() -> None:
    await init_models()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    dp.error.register(global_error_handler)

    dp.include_router(admin_router)
    dp.include_router(admin_fallback_router)
    dp.include_router(client_router)

    logger.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")
