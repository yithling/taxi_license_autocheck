from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from bot.config import *  # Импорт конфигурации
from bot.db import db  # Импорт работы с базой данных

# Создаем роутер для обработки команд
router = Router()

# Определяем состояния для FSM (Finite State Machine)
class ClientData(StatesGroup):
    client_name = State()  # Состояние для имени клиента
    client_phone_number = State()  # Состояние для номера телефона
    client_car_number = State()  # Состояние для номера машины


# Обработчик команды /add для начала ввода данных клиента
@router.message(Command("add"))
async def get_client_name(msg: Message, state: FSMContext) -> None:
    """
    Начинает процесс добавления клиента.
    Переводит FSM в состояние ожидания имени клиента.
    """
    await state.set_state(ClientData.client_name)  # Устанавливаем состояние
    await msg.answer("Укажите имя клиента")  # Запрашиваем имя клиента


# Обработчик для получения имени клиента
@router.message(ClientData.client_name)
async def get_phone_number(msg: Message, state: FSMContext) -> None:
    """
    Сохраняет имя клиента и запрашивает номер телефона.
    """
    # Сохраняем имя клиента в состоянии FSM
    await state.update_data(client_name=msg.text)
    # Переводим FSM в состояние ожидания номера телефона
    await state.set_state(ClientData.client_phone_number)
    await msg.answer("Укажите номер телефона клиента")


# Обработчик для получения номера телефона клиента
@router.message(ClientData.client_phone_number)
async def get_car_number(msg: Message, state: FSMContext) -> None:
    """
    Сохраняет номер телефона клиента и запрашивает номер машины.
    """
    # Сохраняем номер телефона в состоянии FSM
    await state.update_data(client_phone_number=msg.text)
    # Переводим FSM в состояние ожидания номера машины
    await state.set_state(ClientData.client_car_number)
    await msg.answer("Укажите номер машины клиента в русской раскладке!")


# Обработчик для получения номера машины и сохранения данных
@router.message(ClientData.client_car_number)
async def save_data(msg: Message, state: FSMContext) -> None:
    """
    Сохраняет номер машины клиента, завершает FSM и добавляет данные в базу.
    """
    # Сохраняем номер машины в состоянии FSM
    await state.update_data(client_car_number=msg.text)
    # Получаем все данные, сохраненные в FSM
    data = await state.get_data()
    # Очищаем состояние FSM
    await state.clear()
    
    # Добавляем данные клиента в базу
    try:
        db.add_to_db(data)  # Передаем данные в базу
        await msg.answer("Данные клиента сохранены")  # Уведомляем пользователя
    except Exception as e:
        # Обрабатываем возможные ошибки при добавлении в базу
        await msg.answer(f"Произошла ошибка при сохранении данных - {e}")
