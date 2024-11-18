import os
import logging
import sys
import tomllib
from flask import Flask, render_template, session
from .mainmenu import mainmenu_blueprint
from .auth import auth_blueprint, auth_key_name
from .requests import requests_blueprint
from .external import external_blueprint
from .clients import clients_blueprint
from .reports import reports_blueprint


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
    
    app.register_blueprint(mainmenu_blueprint, url_prefix="/")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(requests_blueprint, url_prefix="/requests")
    app.register_blueprint(external_blueprint, url_prefix="/external")
    app.register_blueprint(clients_blueprint, url_prefix="/clients")
    app.register_blueprint(reports_blueprint, url_prefix="/reports")


    return app


def load_config(app: Flask, file: str):
    logger = logging.getLogger(__name__)
    logger.info("Loading config...")
    app.config.from_file(file, load=tomllib.load, text=False)

    if app.config["SECRET_KEY"] == "random":
        app.config["SECRET_KEY"] = os.urandom(12)
