from os import path
from flask import (
    Blueprint,
    session,
    render_template,
)

module_path = path.dirname(path.abspath(__file__))
mainmenu_blueprint = Blueprint(
    "mainmenu_bp", __name__, template_folder=path.join(module_path, "web"))


@mainmenu_blueprint.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html", authorized=session["user_name"], internal=session["user_type"] == "internal")
    return render_template("index.html")
