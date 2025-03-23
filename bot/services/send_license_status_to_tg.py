from aiogram import Router


from bot.config import *
from bot.db import db

router = Router()

def check_record_in_car_number_list(car_number) -> bool:
    """Если машина уже проверялась, то добавляем в список, чтобы не дубилровать сообщения"""
    with open(CAR_NUMBER_LIST_PATH, "r") as file:
        lines = file.readlines()

    if car_number + "\n" in lines:
        return False

    with open(CAR_NUMBER_LIST_PATH, "a") as file:
        file.write(car_number + "\n")
        return True


async def send_message_to_tg(bot) -> None:
    """Проверяем в базе данных статус по машинам, если готово, отправляем данные в тг канал"""
    channel_id = CHANNEL_ID
    licenses_data = db.show_db()
    for data in licenses_data:
        #Если вышла полностью
        if data[-1] == "Ready":
            await bot.send_message(channel_id, 
                                    f"{data[1]}\n{data[2]}\n{data[3]}\n\nГотово\n")
            db.delete_record_from_db(data[0])

        elif data[-1] == "Car":
            #Если вышла только на машину
            car_number = data[3].strip()
            if check_record_in_car_number_list(car_number):
                await bot.send_message(channel_id,
                                        f"{data[1]}\n{data[2]}\n{data[3]}\n\n Лицензия на машину\n")
