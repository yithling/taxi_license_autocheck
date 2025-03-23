from bot.config import *
from bot.services.mosru_license import (CarLicense, CarierLicense)

from bot.db import db


def check_car_license(driver, car_number):
    """mosru лицензия на машину"""
    url = MOSRU_CAR_LICENSE_URL.format(car_number)
    try:
        license = CarLicense(driver, url, car_number)
        license_data = license.extract_license_data()
        if license_data["Статус"].strip() == "Действующий":
            return True
    except:
        return False


def check_carier_license(driver, car_number):
    """mosru лицензия на перевозчика"""
    url = MOSRU_CARIER_LICENSE_URL.format(car_number)
    try:
        license = CarierLicense(driver, url, car_number)
        license_data = license.extract_license_data()
        registry_status = license_data["Номера записей в региональном реестре легковых такси города Москвы, содержащих сведения о легковых такси, используемых перевозчиком легковым такси для осуществления перевозок пассажиров и багажа легковым такси:"]
        if car_number in registry_status.split():
            db.add_to_registry_to_db(car_number, "Added")
        if license_data["Статус"].strip() == "Действующий":
            return True
    except:
        return False
