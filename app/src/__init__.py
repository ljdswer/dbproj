import os
import logging
import sys
import tomllib
from flask import Flask, render_template, session


def create_app():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logger = logging.getLogger(__name__)
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder="web/static",
        template_folder="web/templates",
    )
    load_config(app, "config")
    logger.info("Starting app...")

    with app.app_context():
        from .mainmenu import mainmenu_blueprint
        from .auth import auth_blueprint, auth_key_name
        from .requests import requests_blueprint
        from .external import external_blueprint
        from .clients import clients_blueprint
        from .reports import reports_blueprint
    
        app.register_blueprint(mainmenu_blueprint, url_prefix="/")
        app.register_blueprint(auth_blueprint, url_prefix="/auth")
        app.register_blueprint(requests_blueprint, url_prefix="/requests")
        app.register_blueprint(external_blueprint, url_prefix="/external")
        app.register_blueprint(clients_blueprint, url_prefix="/clients")
        app.register_blueprint(reports_blueprint, url_prefix="/reports")
    return app


def load_config(app: Flask, path: str):
    logger = logging.getLogger(__name__)
    logger.info("Loading config...")

    for file in os.listdir(path):
        logger.info(f"Loading config file {file}...")
        with open(f"{path}/{file}", "rb") as f:
            app.config.update(tomllib.load(f))

    if app.config["SECRET_KEY"] == "random":
        app.config["SECRET_KEY"] = os.urandom(12)
