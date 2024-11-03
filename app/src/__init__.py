import os
import logging
import sys
import tomllib
from flask import Flask, render_template, session
from .auth import auth_blueprint, auth_key_name
from .requests import requests_blueprint


def create_app():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logger = logging.getLogger(__name__)
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder="web/static",
        template_folder="web/templates",
    )
    load_config(app, "config.toml")
    logger.info("Starting app...")

    @app.route("/")
    def index():
        if auth_key_name in session:
            return render_template("index.html", authorized=session["user_name"])
        return render_template("index.html")

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(requests_blueprint, url_prefix="/requests")
    return app


def load_config(app: Flask, file: str):
    logger = logging.getLogger(__name__)
    logger.info("Loading config...")
    app.config.from_file("config.toml", load=tomllib.load, text=False)

    if app.config["SECRET_KEY"] == "random":
        app.config["SECRET_KEY"] = os.urandom(12)
