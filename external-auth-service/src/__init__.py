import sys
import logging
import os
import tomllib
from flask import Flask

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
        from .ext_auth import external_auth_blueprint
        app.register_blueprint(external_auth_blueprint)

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
