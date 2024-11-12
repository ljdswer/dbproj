from flask import (
    Blueprint,
    session,
    render_template,
)

mainmenu_blueprint = Blueprint("mainmenu_bp", __name__)

@mainmenu_blueprint.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html", authorized=session["user_name"], internal=session["user_type"] == "internal")
    return render_template("index.html")