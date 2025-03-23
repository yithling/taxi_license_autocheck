from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from bot.db import db  # Импорт работы с базой данных

# Создаем роутер для обработки команды
router = Router()

# Определяем состояние для FSM (Finite State Machine)
class RecordNum(StatesGroup):
    id_record = State()  # Состояние для ввода ID записи


@router.message(Command("delete"))
async def get_id_record(msg: Message, state: FSMContext) -> None:
    """
    Обработчик команды /delete.
    Запрашивает у пользователя ID записи для удаления.
    """
    await state.set_state(RecordNum.id_record)  # Устанавливаем состояние
    await msg.answer("Укажите номер записи для удаления")  # Запрашиваем ID записи


@router.message(RecordNum.id_record)
async def delete_record(msg: Message, state: FSMContext) -> None:
    """
    Удаляет запись из базы данных по указанному ID.
    """
    client_id = msg.text.strip()  # Получаем введенный ID и удаляем лишние пробелы

    # Проверяем, что введенное значение является числом
    if not client_id.isdigit():
        await msg.answer("Введите корректный номер записи (число).")
        return

    # Преобразуем ID в целое число
    client_id = int(client_id)

    # Очищаем состояние FSM
    await state.clear()

    try:
        # Пытаемся удалить запись из базы данных
        db.delete_record_from_db(client_id)
        await msg.answer(f"Запись с ID {client_id} успешно удалена.")
    except ValueError:
        # Если запись не найдена
        await msg.answer(f"Запись с ID {client_id} не найдена. Используйте /show для отображения базы данных.")
    except Exception as e:
        # Обрабатываем другие возможные ошибки
        await msg.answer(f"Произошла ошибка при удалении записи - {e}.")