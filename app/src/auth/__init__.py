from os import path
from flask import Blueprint, session, request, render_template, current_app, redirect, url_for
from hashlib import sha256
from ..db import SQLProvider, select, DataError

auth_blueprint = Blueprint("auth_bp", __name__)
sql_provider = SQLProvider(path.join(path.dirname(path.abspath(__file__)), 'sql'))


@auth_blueprint.route("/", methods=["GET"])
def index():
    return render_template("auth.html")


@auth_blueprint.route("/", methods=["POST"])
def authenticate():
    login = request.form["user"]
    passwd = request.form["pass"]
    
    if not all([login, passwd]):
        return 400
    hash = sha256(passwd.encode()).hexdigest()
    user = None
    try:
        user = select(current_app.config["DATABASE"], sql_provider.get('get_user.sql'), (login,))
    except DataError:
        return render_template("auth.html", message='Некорректрый запрос')

    if len(user) < 1:
        return render_template("auth.html", message='Пользователь не найден')
    
    if hash != user[0][0]:
        return render_template("auth.html", message='Неверный пароль')

    session["group"] = user[0][1]
    
    return redirect(url_for('index'))
