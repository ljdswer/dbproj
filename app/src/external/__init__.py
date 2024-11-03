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
from .model import get_remain
from ..auth import auth_decorator

module_path = path.dirname(path.abspath(__file__))
external_blueprint = Blueprint(
    "external_bp", __name__, template_folder=path.join(module_path, "web")
)

@external_blueprint.route("/")
def index():
    requests = [
        ("Назад", url_for("index")),
        ("Остаток на собственых счетах", url_for("external_bp.remain")),
    ]
    return render_template("menu.html", requests=requests)

@external_blueprint.route("/remain", methods=["GET"])
@auth_decorator(
    ["regular"], lambda: url_for("external_bp.index")
)
def remain():
    result = get_remain()

    if not result:
        return render_template(
            "generic_message.html",
            message="У вас нет счетов",
            link=url_for("external_bp.index"),
        )

    return render_template(
        "generic_table.html",
        link=url_for("external_bp.index"),
        columns=["ИД", "Валюта", "Остаток"],
        rows=result,
    )