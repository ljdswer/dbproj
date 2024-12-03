from os import path
from flask import Blueprint, request, jsonify
from .model import *

module_path = path.dirname(path.abspath(__file__))
external_auth_blueprint = Blueprint("external_auth_bp", __name__,)

@external_auth_blueprint.route("/api/get_user_info", methods=["POST"])
def api_get_user_info():
    user_info = get_user_info(request.form)
    if user_info:
        return jsonify(user_info)
    else:
        return jsonify({"error": "Неверный пароль"})