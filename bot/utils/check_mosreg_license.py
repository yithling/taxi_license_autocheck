from bot.config import *
from bot.db import db
from bot.services.mosreg_license import (CarLicense, CarierLicense)


def check_car_license(driver, car_number) -> bool:
    """mosreg лицензия на машину"""
    url = MOSREG_CAR_LICENSE_URL.format(car_number)
    try:
        license = CarLicense(driver, url)
        license_data = license.extract_license_data()
        if license_data["Статус:"].strip() == "Действующее":
            inn_number = license_data["ИНН:"].strip()
            registry_status = license_data["Внесено в разрешение перевозчика:"].strip()
            if registry_status.isdigit():
                db.add_to_registry_to_db(car_number, "Added")
            #Проверяем, внесено ли в реестр перевозчика, если да, то отправляем данные в дб
            db.add_inn_to_db(inn_number, car_number)
            return True
    except:
        return False


def check_carier_license(driver, inn_number) -> bool:
    """mosreg лицензия перевозчика"""
    url = MOSREG_CARIER_LICENSE_URL.format(inn_number)
    try:
        license = CarierLicense(driver, url)
        license_data = license.extract_license_data()
        if license_data["Статус:"].strip() == "Действующее":
            return True
    except:
        return False