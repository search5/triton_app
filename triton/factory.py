from flask import Flask
import yaml


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_file(config_filename, load=yaml.safe_load)

    from triton.models import db
    db.init_app(app)

    return app
    