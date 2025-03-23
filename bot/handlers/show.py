from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.db import db  # Импорт работы с базой данных

# Создаем роутер для обработки команды
router = Router()

@router.message(Command("show"))
async def show(msg: Message) -> None:
    """
    Обработчик команды /show.
    Отправляет пользователю список записей из базы данных.
    """
    try:
        # Отправляем сообщение о начале вывода данных
        await msg.answer("Список лицензий на проверку:")

        # Получаем список записей из базы данных
        db_list = db.show_db()

        # Проверяем, есть ли записи в базе данных
        if not db_list:
            await msg.answer("База данных пуста.")
            return

        # Формируем текст для отправки
        result = []
        for data in db_list:
            id_db, client_name, client_phone_number, client_car_number = data[:4]
            result.append(
                f"<b>Номер записи:</b> {id_db}\n"
                f"<b>Имя клиента:</b> {client_name}\n"
                f"<b>Номер телефона:</b> {client_phone_number}\n"
                f"<b>Номер машины:</b> {client_car_number}\n"
            )

        # Отправляем все записи одним сообщением
        await msg.answer("\n\n".join(result), parse_mode="HTML")

    except Exception as e:
        # Обрабатываем возможные ошибки
        await msg.answer(f"Произошла ошибка при получении данных - {e}.")

