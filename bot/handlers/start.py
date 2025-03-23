from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start(msg: Message) -> None:
    """
    Обработчик команды /start.
    Отправляет пользователю приветственное сообщение с инструкцией.
    """

    await msg.answer("""
Для получения списка комманд, используйте /help.
    """)
