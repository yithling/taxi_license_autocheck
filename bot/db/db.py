import sqlite3

from bot.config import *


db = sqlite3.connect(DB_PATH)
cursor = db.cursor()


def connect_to_db() -> None:
    """Подключается к базе, и создает таблицу если ее не существует"""
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS Clients(
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT, 
                client_phone_number TEXT, 
                client_car_number TEXT,
                region TEXT,
                inn_number TEXT,
                registry_status TEXT,
                status TEXT
                )
                """)
    
    cursor.execute("SELECT * FROM Clients")

        
def insert_to_db(client_data) -> None:
    """Добавляет клиента в базу"""
    cursor = db.cursor()
    cursor.execute("""
                   INSERT 
                   INTO Clients(client_name, client_phone_number, client_car_number)
                   VALUES(?,?,?)"""
                   , (client_data))
    db.commit()


def delete_record_from_db(client_id) -> None:
    """Удаляет запись из базы"""
    connect_to_db()
    client_id = int(str(client_id).strip())
    cursor.execute("""
                   DELETE 
                   FROM Clients 
                   WHERE client_id=?"""
                   , (client_id, ))
    db.commit()


def clean_table() -> None:
    """Очищает таблицу"""
    connect_to_db()
    cursor.execute("""DELETE FROM Clients""")
    db.commit()


def close_db() -> None:
    """Закрывает базу"""
    cursor.close()
    db.close()


def show_db() -> list:
    """Показывает все записи в базе"""
    connect_to_db()
    db_records = cursor.fetchall()
    return db_records


def add_to_db(data) -> None:
    """Добавляет данные в базу"""
    connect_to_db()
    client_data = tuple(value for value in data.values())
    insert_to_db(client_data)


def add_region_to_db(region, car_number) -> None:
    """Добавляет регион в базу"""
    id = get_id_client(car_number)
    connect_to_db()
    cursor.execute("""
                   UPDATE Clients
                   SET region=? 
                   WHERE client_id=?"""
                   , (region, id))
    db.commit()


def add_inn_to_db(inn_number, car_number) -> None:
    """Добавляет ИНН в базу"""
    id = get_id_client(car_number)
    connect_to_db()
    cursor.execute("""
                   UPDATE Clients 
                   SET inn_number=?
                   WHERE client_id=?"""
                   , (inn_number, id))
    db.commit()


def add_to_registry_to_db(car_number, status) -> None:
    """Добавляет реестр в базу"""
    id = get_id_client(car_number)
    connect_to_db()
    cursor.execute("""
                   UPDATE Clients
                   SET registry_status=?
                   WHERE client_id=?"""
                   , (status, id))
    db.commit()


def add_license_status(car_number, status) -> None:
    """Добавляет статус лицензии в базу"""
    id = get_id_client(car_number)
    connect_to_db()
    cursor.execute("""
                   UPDATE Clients 
                   SET status=?
                   WHERE client_id=?"""
                   , (status, id))
    db.commit()

def get_id_client(car_number) -> str:
    """Получает id клиента по номеру машины"""
    connect_to_db()
    cursor.execute("""
                   SELECT * 
                   FROM Clients 
                   WHERE client_car_number=?"""
                   , (car_number,))
    data = cursor.fetchall()
    db.commit()
    return data[0][0]


def get_car_numbers() -> list:
    """Получает все номера машин из базы"""
    connect_to_db()
    cursor.execute("""
                   SELECT client_car_number 
                   FROM Clients""")

    return cursor.fetchall()


def get_inn_number(car_number):
    """Получает ИНН клиента по номеру машины"""

    cursor.execute("""
                SELECT inn_number
                From Clients
                WHERE client_car_number=?"""
                , (car_number,))
    inn_number = cursor.fetchall()[0][0]
    db.commit()
    return inn_number
    

def get_registry_status(car_number):
    """Получает статус реестра по номеру машины"""
    cursor.execute("""
                    SELECT registry_status
                    FROM Clients
                    WHERE client_car_number=?"""
                    , (car_number,))
    status = cursor.fetchall()[0][0]
    db.commit()
    return status
                   



