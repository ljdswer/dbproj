from flask import session, current_app, render_template, request
from os import path
from hashlib import sha256
from dataclasses import dataclass
from typing import List, Union
from functools import wraps
import requests

from ..db import SQLProvider, select, DataError

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))

def auth_decorator(url_back):
    def inner_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return render_template(
                    "generic_message.html",
                    message="Вы не авторизованы",
                    link=url_back(),
                )
            group = session["user_role"]
            groups = current_app.config["PERMISSIONS"][request.endpoint]
            if group not in groups:
                return render_template(
                    "generic_message.html",
                    message="Ваша учётная запись не обладает достаточным уровнем доступа",
                    link=url_back(),
                )

            response = f(*args, **kwargs)
            return response

        return wrapped

    return inner_decorator

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

def perform_login_internal(login, passwd) -> AuthResult:
    sql = sql_provider.get("get_user_internal.sql")
    user = None
    try:
        user = select(
            current_app.config["DATABASE"]["auth"], sql, (login,)
        )
    except DataError:
        return AuthErr("Данные запроса некорректны")

    if len(user) < 1:
        return AuthErr("Пользователь не найден")

    hash = sha256(passwd.encode()).hexdigest()
    if hash != user[0]["user_pass_hash"]:
        return AuthErr("Неверный пароль")

    session["user_id"] = user[0]["user_id"]
    session["user_name"] = login
    session["user_role"] = user[0]["user_role"]
    session["user_type"] = "internal"
    return AuthOk

def perform_login_external(login, passwd) -> AuthResult:
    request = requests.post(
        current_app.config["EXTERNAL_AUTH"]["url"],
        {"login": login, "passwd": passwd},    
    )
    try:
        json = request.json()[0]
        if "error" in json:
            return AuthErr(json["error"])
        session["user_id"] = json["user_id"]
        session["user_role"] = json["user_role"]
        session["user_name"] = login
        session["agreement_no"] = json["agreement_no"]
        session["user_type"] = "external"
    except:
        return AuthErr("Неизвестная ошибка")
    return AuthOk
    

def perform_login(login, passwd, priv) -> AuthResult:
    if not all([login, passwd]):
        return AuthErr("Аргументы не соответствуют запросу")

    sql = None
    user_type = None
    if priv == "on":
        return perform_login_internal(login, passwd)
    else:
        return perform_login_external(login, passwd)