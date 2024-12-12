from logging import getLogger
from typing import Union
from os import path
from flask import current_app
from ..db import SQLProvider, DataError, select

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))

def get_login_info(request) -> Union[None, list]:
    logger = getLogger(__name__)
    login = request.get("login")
    passwd = request.get("passwd")
    if not all([login, passwd]):
        logger.error("A server sent illegal request to the external auth service")
        return None
    return [login, passwd]

def get_user_info(request) -> Union[None, dict]:
    linfo = get_login_info(request)

    if not linfo:
        return None

    login, passwd = linfo
    sql = sql_provider.get("get_user_external.sql")
    data = None
    try:
        data = select(
            current_app.config["DATABASE"]["auth"], sql, (login, passwd)
        )
    except DataError:
        return None
    if len(data) < 1:
        return None
    return data[0]
