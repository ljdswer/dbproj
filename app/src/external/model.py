from ..db import SQLProvider, DataError, select, DBContextManager
from ..utils import Result, fetch_from_cache
from flask import current_app, session
from typing import Optional
from os import path
from logging import getLogger
from decimal import Decimal

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))

def get_remain(agreement) -> Optional[list]:
    sql = sql_provider.get("remain.sql")
    accounts = select(current_app.config["DATABASE"]["external"], sql, (agreement,))
    if len(accounts) < 1:
        return None
    return [(i["account_id"], i["currency"], i["leftover"]) for i in accounts]

@fetch_from_cache(current_app.config["CACHE"], 300)
def get_own_accounts(agreement) -> Optional[list]:
    sql = sql_provider.get("get_accounts_by_agreement.sql")
    accounts = select(current_app.config["DATABASE"]["external"], sql, (agreement,))
    if len(accounts) < 1:
        return None
    return [i["account_id"] for i in accounts]

def transfer_between_own(form_data) -> Result:
    if not all([form_data.get("src_account_id"), form_data.get("dst_account_id"), form_data.get("amount")]):
        return Result(error="Не все поля заполнены")

    owns = sql_provider.get("check_if_client_owns_account.sql")
    leftover = sql_provider.get("get_leftover.sql")
    history = sql_provider.get("insert_history.sql")
    try:
        with DBContextManager(current_app.config["DATABASE"]["external"]) as cur:
            cur.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            cur.connection.begin()
            
            # Check if client owns the source account
            cur.execute(owns, (session["agreement_no"], form_data["src_account_id"]))
            result = cur.fetchone()
            if not result:
                return Result(error="Счёт не найден")
            
            # Check if client owns the source account
            cur.execute(owns, (session["agreement_no"], form_data["dst_account_id"]))
            result = cur.fetchone()
            if not result:
                return Result(error="Счёт не найден")

            # Check if client has enough money on the source account
            cur.execute(leftover, (form_data["src_account_id"], ))
            result = cur.fetchone()[0]
            if (Decimal(result) < Decimal(form_data["amount"])):
                return Result(error="Недостаточно средств")

            # Insert a row to the acc_history which will trigger money transfer
            cur.execute(history, (session["agreement_no"], form_data["src_account_id"], form_data["dst_account_id"], form_data["amount"]))

            # Just for clarity, DBContextManager will commit the transaction regardless
            cur.connection.commit()
    except DataError:
        return Result(error="Запрос некорректен")
    return Result(value="Транзакция успешно выполнена")