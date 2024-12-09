from os import path
from flask import (
    Blueprint,
    session,
    request,
    render_template,
    url_for,
)

from ..auth import auth_decorator, auth_key_name
from .model import *

module_path = path.dirname(path.abspath(__file__))
requests_blueprint = Blueprint(
    "requests_bp", __name__, template_folder=path.join(module_path, "web")
)

@requests_blueprint.route("/")
def index():
    requests = [
        ("Назад", url_for("mainmenu_bp.index")),
        ("Клиент - Сумма - Число счетов", url_for("requests_bp.moneyperclient")),
        ("Счета с последним изменением остатка за период", url_for("requests_bp.accountsfromtodate")),
    ]
    return render_template("requests.html", requests=requests)


@requests_blueprint.route("/stat_moneyperclient", methods=["GET"])
@auth_decorator(lambda: url_for("requests_bp.index"))
def moneyperclient():
    result = get_moneyperclient()
    if not result:
        return render_template(
            "generic_message.html",
            message="Нет данных",
            link=url_for("requests_bp.index"),
        )
    return render_template(
        "generic_table.html",
        link=url_for("requests_bp.index"),
        columns=["№ Договора", "Сумма на счетах", "Число счетов"],
        rows=result,
    )


@requests_blueprint.route("/stat_accountsfromtodate", methods=["GET", "POST"])
@auth_decorator(lambda: url_for("requests_bp.index"))
def accountsfromtodate():
    if request.method == "GET":
        return render_template("accounts_from_to_date.html")
    date_from = request.form["date_from"]
    date_to = request.form["date_to"]

    result = get_accountsfromtodate(date_from, date_to)

    if result.is_err():
        return render_template("generic_message.html", link=request.url_rule, message=result.error)
        
    return render_template(
        "generic_table.html",
        columns=["ИД", "Валюта", "Остаток", "Дата установления остатка"],
        rows=result.value,
    )
