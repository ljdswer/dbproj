from flask import current_app
from ..db import SQLProvider, select, DataError
from os import path
from typing import Optional

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))

def get_moneyperclient() -> Optional[list]:
    sql = sql_provider.get("money_per_client.sql")
    stats = select(current_app.config["DATABASE"], sql, ())
    if len(stats) < 1:
        return None
    return [(i["agreement_no"], i["sum"], i["amount_of_accounts"]) for i in stats]

def get_accountsfromtodate(date_from, date_to) -> Optional[list]:
    if not all([date_from, date_to]):
        return None

    sql = sql_provider.get("accounts_from_to_date.sql")
    result = None
    try:
        result = select(
            current_app.config["DATABASE"],
            sql,
            (
                date_from,
                date_to,
            ),
        )
    except DataError:
        return None

    return [(i["account_id"], i["currency"], i["leftover"], i["leftover_assign_date"]) for i in result]
