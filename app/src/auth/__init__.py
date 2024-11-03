from os import path
from flask import (
    Blueprint,
    session,
    request,
    render_template,
    redirect,
    url_for,
)
from .model import *

module_path = path.dirname(path.abspath(__file__))
auth_blueprint = Blueprint(
    "auth_bp", __name__, template_folder=path.join(module_path, "web")
)
auth_key_name = "user_id"


@auth_blueprint.route("/", methods=["GET"])
def index():
    return render_template("auth.html")


@auth_blueprint.route("/", methods=["POST"])
def authenticate():
    login = request.form["user"]
    passwd = request.form["pass"]
    priv = request.form.get("priv") or "off"

    result = perform_login(login, passwd, priv)
    if isinstance(result, AuthErr):
        return render_template("auth.html", message=result.error)
    return redirect(url_for("index"))


@auth_blueprint.route("/logout")
def logout():
    clear_login()
    return redirect(url_for("index"))
