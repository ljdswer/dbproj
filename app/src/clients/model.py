from os import path
from flask import current_app
from typing import List
from ..db import SQLProvider, select, alter, DataError
from ..utils import Result

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))

def list_clients() -> Result[List]:
    sql = sql_provider.get("list_clients.sql")
    result = None
    try:
        result = select(
            current_app.config["DATABASE"]["clients"],
            sql,
            (),
        )
    except DataError:
        return Result(error="Запрос некорректен")
    return Result(value=[(i["agreement_no"], i["last_name"], i["date_of_birth"], i["address"], i["phone_no"]) for i in result])
    
def edit_client(agreement_no: int, last_name: str, date_of_birth: str, address: str, phone_no: str) -> Result[None]:
    if not all([agreement_no, last_name, date_of_birth, address, phone_no]):
        return Result(error="Не все поля заполнены")

    sql = sql_provider.get("edit_client.sql")
    try:
        alter(
            current_app.config["DATABASE"]["clients"],
            sql,
            (last_name, date_of_birth, address, phone_no, agreement_no),
        )
    except DataError:
        return Result(error="Запрос некорректен")
    except:
        return Result(error="Произошла непредвиденная ошибка")
    return Result(value=None)

def create_client(agreement_no: int, last_name: str, date_of_birth: str, address: str, phone_no: str) -> Result[None]:
    if not all([agreement_no, last_name, date_of_birth, address, phone_no]):
        return Result(error="Не все поля заполнены")
    sql = sql_provider.get("create_client.sql")
    try:
        alter(
            current_app.config["DATABASE"]["clients"],
            sql,
            (agreement_no, last_name, date_of_birth, address, phone_no),
        )
    except DataError:
        return Result(error="Запрос некорректен")
    except:
        return Result(error="Произошла непредвиденная ошибка")
    return Result(value=None)