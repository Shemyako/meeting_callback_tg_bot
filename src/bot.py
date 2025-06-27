import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent

from .cache import ConferenceCache
from .config import TG_BOT_TOKEN
from .exceptions import MeetCallbackError
from .handlers import router
from .log import logger

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


@dp.error()
async def global_error_handler(event: ErrorEvent) -> None:
    exception = event.exception
    update = event.update
    logger.error(f"An error occurred: {exception}")
    if update.message:
        if isinstance(exception, MeetCallbackError):
            await update.message.reply(
                f"Получена ошибка: {exception.message}\nСвяжитесь с администратором",
            )
        else:
            await update.message.reply(
                "Произошла ошибка. Напишите администратору или попробуйте позже.",
            )


async def main() -> None:
    await ConferenceCache.refresh_config()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
