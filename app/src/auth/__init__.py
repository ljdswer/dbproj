from os import path
from functools import wraps
from flask import (
    Blueprint,
    session,
    request,
    render_template,
    current_app,
    redirect,
    url_for,
)
from hashlib import sha256
from ..db import SQLProvider, select, DataError


def group_by_user(user_id):
    try:
        return select(
            current_app.config["DATABASE"],
            sql_provider.get("group_by_user.sql"),
            (user_id, ),
        )[0][0]
    except DataError:
        return None
    except IndexError:
        return None


def auth_decorator(groups: list, url_back):
    def inner_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if auth_key_name not in session:
                return render_template(
                    "generic_message.html",
                    message="Вы не авторизованы",
                    link=url_for("requests_bp.index"),
                )
            group = group_by_user(session[auth_key_name])
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


module_path = path.dirname(path.abspath(__file__))
auth_blueprint = Blueprint(
    "auth_bp", __name__, template_folder=path.join(module_path, "web")
)
sql_provider = SQLProvider(path.join(module_path, "sql"))
auth_key_name = "user_id"


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
        user = select(
            current_app.config["DATABASE"], sql_provider.get("get_user.sql"), (login,)
        )
    except DataError:
        return render_template("auth.html", message="Некорректрый запрос")

    if len(user) < 1:
        return render_template("auth.html", message="Пользователь не найден")

    if hash != user[0][0]:
        return render_template("auth.html", message="Неверный пароль")

    session[auth_key_name] = user[0][1]
    session["user_name"] = login
    return redirect(url_for("index"))


@auth_blueprint.route("/logout")
def logout():
    if auth_key_name in session:
        session.pop(auth_key_name)
    return redirect(url_for("index"))
