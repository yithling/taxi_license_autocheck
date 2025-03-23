import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# --- Переменные для Telegram ---
TELEGRAM_TOKEN = str(os.getenv("TELEGRAM_BOT_TOKEN"))
CAPTCHA_TOKEN = str(os.getenv("CAPTCHA_TOKEN"))
CHANNEL_ID = str(os.getenv("TELEGRAM_CHANNEL_ID"))

# --- Пути к файлам и базе данных ---
DB_PATH = "./bot/db/db.db"
CAPTCHA_FILE_PATH = "./bot/images/captcha.png"
QR_FILE_PATH = "./bot/images/qr.png"
CAR_NUMBER_LIST_PATH = "./bot/car_number_list.txt"

# --- URL-адреса для работы с лицензиями ---
MOSREG_CAR_LICENSE_URL = "https://mtdi.mosreg.ru/taxi-cars?licenseNumber=&inn=&name=&gosNumber={}&region=ALL"
MOSREG_CARIER_LICENSE_URL = "https://mtdi.mosreg.ru/taxi-permits?licenseNumber=&inn={}&name=&region=ALL"
MOSRU_CAR_LICENSE_URL = "https://transport.mos.ru/auto/reestr_taxi"
MOSRU_CARIER_LICENSE_URL = "https://transport.mos.ru/auto/reestr_carrier"
