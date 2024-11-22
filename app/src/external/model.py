from ..db import SQLProvider, select
from flask import current_app, session
from typing import Optional
from os import path

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))

def get_remain() -> Optional[list]:
    sql = sql_provider.get("remain.sql")
    accounts = select(current_app.config["DATABASE"]["external"], sql, (session["user_id"],))
    if len(accounts) < 1:
        return None
    return [(i["account_id"], i["currency"], i["leftover"]) for i in accounts]