from ..db import SQLProvider, DataError, select, callproc
from ..utils import Result
from flask import current_app, session
from typing import Optional
from os import path
from logging import getLogger

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))

def get_remain() -> Optional[list]:
    sql = sql_provider.get("remain.sql")
    accounts = select(current_app.config["DATABASE"]["external"], sql, (session["agreement_no"],))
    if len(accounts) < 1:
        return None
    return [(i["account_id"], i["currency"], i["leftover"]) for i in accounts]

def get_own_accounts() -> Optional[list]:
    sql = sql_provider.get("get_accounts_by_agreement.sql")
    accounts = select(current_app.config["DATABASE"]["external"], sql, (session["agreement_no"],))
    if len(accounts) < 1:
        return None
    return [i["account_id"] for i in accounts]

def transfer_between_own(form_data) -> Result:
    if not all([form_data.get("src_account_id"), form_data.get("dst_account_id"), form_data.get("amount")]):
        return Result(error="Не все поля заполнены")

    sql = sql_provider.get("transfer_between_own.sql")
    result = None
    try:
        result = callproc(current_app.config["DATABASE"]["external"], sql,
            (session["agreement_no"], form_data["src_account_id"], form_data["dst_account_id"], form_data["amount"]))[0]["Status"]
    except DataError:
        return Result(error="Запрос некорректен")

    if result == "ACCOUNTNOTFOUND":
        return Result(error="Не найден счет")
    elif result == "NOTENOUGH":
        return Result(error="Недостаточно средств")
    elif result == "SUCCESS":
        return Result(value=None)
    
    logger = getLogger(__name__)
    logger.error(f"Unknown error from procedure: {result}")
    return Result(error="Неизвестная ошибка")