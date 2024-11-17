from os import path
from flask import (
    Blueprint,
    session,
    request,
    render_template,
    url_for,
    jsonify,
    redirect
)

from ..auth import auth_decorator, auth_key_name
from .model import *

module_path = path.dirname(path.abspath(__file__))
clients_blueprint = Blueprint(
    "clients_bp", __name__, template_folder=path.join(module_path, "web")
)


@clients_blueprint.route("/", methods=["GET"])
@auth_decorator(lambda: url_for("mainmenu_bp.index"))
def index():
    result = list_clients()
    if result.is_err():
        return render_template(
            "generic_message.html",
            message=result.error,
            link=url_for("mainmenu_bp.index"),
        )
    return render_template(
        "clients.html",
        rows=result.value,
    )


@clients_blueprint.route("/edit", methods=["POST"])
@auth_decorator(lambda: url_for("mainmenu_bp.index"))
def edit():
    fields = request.form.to_dict()
    result = edit_client(
        fields["agreement_no"],
        fields["last_name"],
        fields["date_of_birth"],
        fields["address"],
        fields["phone_no"],
    )
    if result.is_err():
        return jsonify(error=result.error), 400
    return jsonify("OK")


@clients_blueprint.route("/create", methods=["POST"])
@auth_decorator(lambda: url_for("mainmenu_bp.index"))
def create():
    fields = request.form.to_dict()
    result = create_client(
        fields["agreement_no"],
        fields["last_name"],
        fields["date_of_birth"],
        fields["address"],
        fields["phone_no"],
    )

    if result.is_err():
        return render_template(
            "generic_message.html",
            message=result.error,
            link=url_for("clients_bp.index"),
        )
    return redirect(url_for("clients_bp.index"))