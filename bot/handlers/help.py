from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

# Создаем роутер для обработки команды
router = Router()

@router.message(Command("help"))
async def help(msg: Message) -> None:
    """
    Обработчик команды /help.
    Отправляет пользователю список доступных команд.
    """
    # Формируем текст ответа
    help_text = """
<b>Список доступных команд:</b>
/start - Включить бот.
/help - Список команд.
/add - Добавить запись в базу данных.
/show - Показать записи в базе данных.
/delete - Удалить запись из базы данных (указать номер записи).
/clean - Удалить все записи из базы данных.
"""

    # Отправляем сообщение с форматированием
    await msg.answer(help_text, parse_mode="HTML")