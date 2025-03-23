import asyncio
import schedule

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bot.config import *
from bot.db import db
from bot.services import send_license_status_to_tg
from bot.utils import (check_mosreg_license, check_mosru_license)



def check_car_license(driver, car_number) -> bool:
    """Проверяем лицензию на машину"""
    if check_mosreg_license.check_car_license(driver, car_number):
        db.add_region_to_db("Московская область", car_number)
        return True
    elif check_mosru_license.check_car_license(driver, car_number):
        db.add_region_to_db("Москва", car_number)
        return True
    else:
        return False


def check_carier_license(driver, car_number) -> bool:
    """Проверяем лицензию на перевозчка"""
    inn_number = db.get_inn_number(car_number)
    if inn_number is not None:
        return check_mosreg_license.check_carier_license(driver, inn_number)
    if check_mosru_license.check_carier_license(driver, car_number):
        return True
    return False


def check_licenses():
    """Проверяем лицензию по номеру машины"""
    car_number_list = db.get_car_numbers()
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    for car_number in car_number_list:
        car_number = car_number[0].strip()
        #Если лицензия гна машину есть
        if check_car_license(driver, car_number):
            #Проверяем лицензию на перевозчка
            if check_carier_license(driver, car_number):
                #Если она тоже есть и лицензия на машину привязана к перовзчику, то ставим статус Ready
                registry_status = db.get_registry_status(car_number)
                if registry_status == "Added":
                    db.add_license_status(car_number, "Ready")
                else:
                    db.add_license_status(car_number, "Car")

            else:
                db.add_license_status(car_number, "Car")
    driver.quit()


async def start_checking(bot):
    schedule.every().day.at("09:55").do(check_licenses)
    schedule.every().day.at("11:30").do(check_licenses)
    schedule.every().day.at("11:30").do(check_licenses)
    schedule.every().day.at("12:00").do(check_licenses)
    schedule.every().day.at("14:30").do(check_licenses)
    schedule.every().day.at("16:30").do(check_licenses)
    schedule.every().day.at("18:00").do(check_licenses)
    schedule.every().day.at("18:30").do(check_licenses)
    while True:
        schedule.run_pending()
        #Отправляем на тг канал
        await send_license_status_to_tg.send_message_to_tg(bot)
        await asyncio.sleep(10)


