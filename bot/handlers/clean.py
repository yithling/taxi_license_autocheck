from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.db import db  # Импорт работы с базой данных

# Создаем роутер для обработки команды
router = Router()

@router.message(Command("clean_all"))
async def clean(msg: Message) -> None:
    """
    Обработчик команды /clean_all.
    Очищает таблицу в базе данных.
    """
    try:
        # Очищаем таблицу в базе данных
        db.clean_table()
        # Отправляем сообщение об успешной очистке
        await msg.answer("Все данные успешно очищены.")
    except Exception as e:
        # Обрабатываем возможные ошибки при очистке таблицы
        await msg.answer(f"Произошла ошибка при очистке данных. - {e}")

