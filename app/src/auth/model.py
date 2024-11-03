from flask import session, current_app
from os import path
from hashlib import sha256
from ..db import SQLProvider, select, DataError

from dataclasses import dataclass
from typing import List, Union

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))

class AuthResult:
    pass

@dataclass
class AuthOk(AuthResult):
    pass

@dataclass
class AuthErr(AuthResult):
    error: str

def clear_login():
    session.clear()

def perform_login(login, passwd, priv) -> AuthResult:
    if not all([login, passwd]):
        return AuthErr("Аргументы не соответствуют запросу")
    hash = sha256(passwd.encode()).hexdigest()

    sql = None
    if priv == "on":
        sql = sql_provider.get("get_user_internal.sql")
    else:
        sql = sql_provider.get("get_user_external.sql")
    
    user = None
    try:
        user = select(
            current_app.config["DATABASE"], sql, (login,)
        )
    except DataError:
        return AuthErr("Данные запроса некорректны")

    if len(user) < 1:
        return AuthErr("Пользователь не найден")

    if hash != user[0]["user_pass_hash"]:
        return AuthErr("Неверный пароль")

    session["user_id"] = user[0]["user_id"]
    session["user_name"] = login
    session["user_role"] = user[0]["user_role"]
    return AuthOk