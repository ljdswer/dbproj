from os import path
from flask import (
    abort,
    Blueprint,
    session,
    request,
    render_template,
    redirect,
    url_for,
    current_app,
)
from ..db import SQLProvider, select, DataError
from ..auth import auth_decorator, auth_key_name

module_path = path.dirname(path.abspath(__file__))
requests_blueprint = Blueprint(
    "requests_bp", __name__, template_folder=path.join(module_path, "web")
)
sql_provider = SQLProvider(path.join(module_path, "sql"))


@requests_blueprint.route("/")
def index():
    requests = [
        ("Назад", url_for("index")),
        ("Остаток на собственых счетах", url_for("requests_bp.remain")),
        ("Клиент - Сумма - Число счетов", url_for("requests_bp.moneyperclient")),
        ("Счета с последним изменением остатка за период", url_for("requests_bp.accountsfromtodate")),
    ]
    return render_template("requests.html", requests=requests)


@requests_blueprint.route("/remain", methods=["GET"])
@auth_decorator(
    ["admin", "manager", "client", "statist"], lambda: url_for("requests_bp.index")
)
def remain():
    sql = sql_provider.get("remains.sql")
    accounts = select(current_app.config["DATABASE"], sql, (session[auth_key_name],))

    if len(accounts) == 0:
        return render_template(
            "generic_message.html",
            message="У вас нет счетов",
            link=url_for("requests_bp.index"),
        )

    return render_template(
        "generic_table.html",
        link=url_for("requests_bp.index"),
        columns=["ИД", "Валюта", "Остаток"],
        rows=[(i[0], i[1], i[2]) for i in accounts],
    )


@requests_blueprint.route("/stat_moneyperclient", methods=["GET"])
@auth_decorator(["admin", "statist"], lambda: url_for("requests_bp.index"))
def moneyperclient():
    sql = sql_provider.get("money_per_client.sql")
    stats = select(current_app.config["DATABASE"], sql, ())
    if len(stats) == 0:
        return render_template(
            "generic_message.html",
            message="Нет данных",
            link=url_for("requests_bp.index"),
        )
    return render_template(
        "generic_table.html",
        link=url_for("requests_bp.index"),
        columns=["№ Договора", "Сумма на счетах", "Число счетов"],
        rows=[(i["agreement_no"], i["sum"], i["amount_of_accounts"]) for i in stats],
    )


@requests_blueprint.route("/stat_accountsfromtodate", methods=["GET", "POST"])
@auth_decorator(["admin", "statist"], lambda: url_for("requests_bp.index"))
def accountsfromtodate():
    if request.method == "GET":
        return render_template("accounts_from_to_date.html")

    date_from = request.form["date_from"]
    date_to = request.form["date_to"]

    if not all([date_from, date_to]):
        abort(400)

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
        return render_template(
            "generic_message.html",
            link=request.url_rule,
            message="Запрос некорректен",
        )

    return render_template(
        "generic_table.html",
        columns=["ИД", "Валюта", "Остаток", "Дата установления остатка"],
        rows=[(i["account_id"], i["currency"], i["leftover"], i["leftover_assign_date"]) for i in result],
    )
