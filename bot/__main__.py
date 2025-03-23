import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.db import db
from bot.config import *
from bot.handlers import (add, clean, delete, help, show, start)
from bot.services import (autocheck, send_license_status_to_tg)



async def main() -> None:
    """
    Основная асинхронная функция для запуска бота.
    """

    bot = Bot(token=TELEGRAM_TOKEN, 
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router, 
        add.router, 
        help.router,
        show.router,
        delete.router, 
        clean.router,
        send_license_status_to_tg.router
    )

    check_license = asyncio.create_task(autocheck.start_checking(bot))

    await asyncio.gather(
        check_license,
        bot.delete_webhook(drop_pending_updates=True),
        dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a")
    asyncio.run(main())
    db.close_db()
