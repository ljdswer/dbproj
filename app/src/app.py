import logging
import sys
import tomllib
from flask import Flask, render_template, request, current_app, abort

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
        return render_template("index.html")
    return app

def load_config(app: Flask, file: str):
    logger = logging.getLogger(__name__)
    logger.info("Loading config...")
    app.config.from_file("config.toml", load=tomllib.load, text=False)
